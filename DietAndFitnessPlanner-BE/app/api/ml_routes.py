from datetime import datetime, timezone
from typing import Any, Dict, List

import re

from fastapi import APIRouter, HTTPException

from app.db.mongo import get_database
from app.api.notification_routes import create_user_notification
from app.services.mlService import (
    food_recognition_service,
    nutrition_prediction_service,
    exercise_personalization_service,
    goal_achievement_service,
    meal_optimization_service,
    performance_tracking_service,
    ml_pipeline_service,
)

router = APIRouter()


def _normalize_email(email: str) -> str:
    return str(email or "").strip().lower()


def _latest_plan_for_email(email: str) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    if not normalized_email:
        return {}

    db = get_database()
    doc = (
        db["plan_history"]
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(1)
    )
    row = next(iter(doc), None)
    return dict(row) if row else {}


def _recent_coach_history(email: str, limit: int = 8) -> List[Dict[str, Any]]:
    normalized_email = _normalize_email(email)
    if not normalized_email:
        return []

    db = get_database()
    cursor = (
        db["coach_messages"]
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(max(1, min(limit, 20)))
    )
    history = list(cursor)
    history.reverse()
    return history


def _summarize_meal_plan(diet_plan: Dict[str, Any]) -> str:
    meal_plan = diet_plan.get("meal_plan", {}) if isinstance(diet_plan, dict) else {}
    if not meal_plan:
        return "I do not have a saved meal plan yet."

    meal_lines: List[str] = []
    for meal_name, meal_data in list(meal_plan.items())[:4]:
        breakdown = meal_data.get("breakdown", {}) if isinstance(meal_data, dict) else {}
        macros = breakdown.get("macros", {}) if isinstance(breakdown, dict) else {}
        meal_lines.append(
            f"{meal_name.title()}: {breakdown.get('name', meal_data.get('overview', 'Meal'))} "
            f"({macros.get('calories', 0)} kcal, {macros.get('protein', 0)}g protein)"
        )
    return " | ".join(meal_lines)


def _extract_focus(message: str) -> str:
    text = message.lower()
    keyword_groups = {
        "meal": ["what should i eat", "meal", "food", "lunch", "breakfast", "dinner", "snack", "meal prep", "recipe"],
        "protein": ["protein", "muscle", "gain", "high protein"],
        "calorie": ["calorie", "weight loss", "fat loss", "cut", "bulk", "deficit", "surplus"],
        "workout": ["workout", "exercise", "training", "gym", "cardio", "split", "lifting"],
        "recovery": ["recovery", "sleep", "rest", "sore", "pain", "injury"],
        "budget": ["budget", "cheap", "affordable", "low cost", "cost"],
        "timeline": ["how long", "timeline", "when will", "weeks", "days", "months"],
        "adherence": ["adhere", "stick to", "follow", "consistency", "compliance"],
        "supplement": ["supplement", "creatine", "whey", "protein powder", "multivitamin"],
    }

    for focus, keywords in keyword_groups.items():
        if any(keyword in text for keyword in keywords):
            return focus
    return "general"


_ABUSIVE_PATTERNS = [
    "idiot",
    "stupid",
    "dumb",
    "shut up",
    "fool",
    "fuck",
    "shit",
    "bitch",
    "asshole",
    "moron",
]


def _contains_abusive_language(message: str) -> bool:
    lowered = message.lower()
    return any(pattern in lowered for pattern in _ABUSIVE_PATTERNS)


def _parse_requested_weeks(message: str) -> float | None:
    lowered = message.lower()
    match = re.search(r"(\d+(?:\.\d+)?)\s*(week|weeks|wk|wks|day|days|month|months)", lowered)
    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2)
    if unit.startswith("day"):
        return value / 7.0
    if unit.startswith("month"):
        return value * 4.0
    return value


def _safety_warning(message: str, current_weight: float | None, target_weight: float | None, goal_key: str) -> str | None:
    lowered = message.lower()
    if any(term in lowered for term in ["starve", "skip meals", "one meal a day", "500 calories", "under 800 calories", "detox", "vomit"]):
        return "That target is too aggressive and not safe. We should keep the plan sustainable with enough protein, calories, and recovery."

    weeks = _parse_requested_weeks(message)
    if weeks is not None and current_weight is not None and target_weight is not None:
        gap = abs(current_weight - target_weight)
        if goal_key == "weight_loss" and gap / max(weeks, 1.0) > 1.0:
            return f"That pace is too fast. Losing {gap:g} kg in about {weeks:g} weeks would be risky, so I’d slow it down and protect muscle and energy."
        if goal_key == "muscle_gain" and gap / max(weeks, 1.0) > 0.75:
            return f"That gain target is too rushed. Building {gap:g} kg in about {weeks:g} weeks is better done with a controlled surplus and progressive training."

    return None


def _clarifying_question(focus: str, current_weight: float | None, target_weight: float | None, goal: str) -> str:
    if current_weight is not None and target_weight is not None:
        return "If you want, I can turn this into a 7-day meal and workout plan next."

    if focus in {"meal", "protein", "calorie"}:
        return f"To make this more exact, tell me your current weight and target weight and I’ll tailor the {goal} strategy."

    if focus in {"workout", "recovery"}:
        return "Tell me your equipment, injury history, and workout days and I’ll tighten the plan."

    return "Share your current weight, target weight, and daily routine so I can make this fully personal."


def _safe_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_weight_context(message: str, profile: Dict[str, Any], plan_doc: Dict[str, Any]) -> Dict[str, float | None]:
    current_weight = _safe_float(profile.get("weight") or profile.get("current_weight") or plan_doc.get("weight"))
    target_weight = _safe_float(profile.get("target_weight") or profile.get("targetWeight") or plan_doc.get("target_weight"))
    numbers = [float(match) for match in re.findall(r"\d+(?:\.\d+)?", message)]
    lowered = message.lower()

    if current_weight is None and numbers:
        current_weight = numbers[0]

    if target_weight is None and numbers:
        if any(token in lowered for token in ["target", "goal", "reach", "from", "to", "down to", "up to"]):
            target_weight = numbers[-1]
        elif len(numbers) >= 2 and any(token in lowered for token in ["lose", "gain", "cut", "bulk", "weightloss", "weight loss"]):
            target_weight = numbers[-1]

    return {"current_weight": current_weight, "target_weight": target_weight}


def _build_strategy_lines(goal: str, focus: str, daily_macros: Dict[str, Any], workout_days: List[str], weight_context: Dict[str, float | None]) -> Dict[str, Any]:
    calories = int(daily_macros.get("calories") or daily_macros.get("daily_calories") or 0)
    protein = int(daily_macros.get("protein") or daily_macros.get("protein_grams") or 0)
    carbs = int(daily_macros.get("carbs") or daily_macros.get("carbs_grams") or 0)
    fats = int(daily_macros.get("fats") or daily_macros.get("fat_grams") or 0)

    current_weight = weight_context.get("current_weight")
    target_weight = weight_context.get("target_weight")
    weight_gap = round((current_weight - target_weight), 1) if current_weight and target_weight else None

    meal_rules = [
        f"Keep daily intake close to {calories} kcal",
        f"Aim for about {protein}g protein across the day",
        f"Use {carbs}g carbs and {fats}g fats as the balance point",
    ]
    workout_rules = [
        "Train 3 to 5 days per week based on recovery",
        "Keep one recovery or light-mobility day each week",
        "Progress slowly instead of chasing extreme volume",
    ]

    if goal == "weight_loss":
        meal_rules.extend([
            "Make protein the anchor in every meal",
            "Keep snacks high-satiety and lower calorie",
        ])
        workout_rules.extend([
            "Use a mix of strength work and low-impact cardio",
            "Track weekly body weight, not daily noise",
        ])
    elif goal == "muscle_gain":
        meal_rules.extend([
            "Add a small calorie surplus instead of overeating",
            "Place carbs around training sessions",
        ])
        workout_rules.extend([
            "Prioritize progressive overload on major lifts",
            "Recover well so strength can move up consistently",
        ])

    weekly_focus = [
        f"Goal focus: {goal.replace('_', ' ')}",
        f"User focus: {focus}",
    ]
    if workout_days:
        weekly_focus.append(f"Workout days: {', '.join(workout_days[:4])}")

    if weight_gap is not None:
        weekly_focus.append(f"Weight gap: {weight_gap} kg")

    check_in = "Check in again after 3 to 5 days with your meals, weight trend, and workout energy."
    if current_weight and target_weight and goal == "weight_loss":
        check_in = f"Your main path is from {current_weight:g} kg to {target_weight:g} kg. Check in weekly with weight trend, hunger, and workout energy."

    return {
        "goal": goal,
        "current_weight": current_weight,
        "target_weight": target_weight,
        "weight_gap": weight_gap,
        "calorie_target": calories,
        "protein_target": protein,
        "weekly_focus": weekly_focus,
        "meal_rules": meal_rules,
        "workout_rules": workout_rules,
        "check_in": check_in,
    }


def _persist_coach_memory(email: str, profile: Dict[str, Any], strategy: Dict[str, Any], focus: str) -> None:
    normalized_email = _normalize_email(email)
    if not normalized_email:
        return

    db = get_database()
    db["users"].update_one(
        {"email": normalized_email},
        {
            "$set": {
                "coach_memory": {
                    "goal": profile.get("goal"),
                    "fitness_level": profile.get("fitnessLevel") or profile.get("fitness_level"),
                    "dietType": profile.get("dietType"),
                    "weight": profile.get("weight") or profile.get("current_weight"),
                    "target_weight": profile.get("target_weight") or profile.get("targetWeight"),
                    "focus": focus,
                    "updated_at": datetime.now(timezone.utc),
                }
            }
        },
        upsert=True,
    )


def _build_coach_reply(email: str, message: str, profile: Dict[str, Any], plan_doc: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
    diet_plan = plan_doc.get("diet_plan", {}) if isinstance(plan_doc, dict) else {}
    fitness_plan = plan_doc.get("fitness_plan", {}) if isinstance(plan_doc, dict) else {}
    focus = _extract_focus(message)
    weight_context = _extract_weight_context(message, profile, plan_doc)

    daily_macros = diet_plan.get("daily_macros", {}) if isinstance(diet_plan, dict) else {}
    meal_plan = diet_plan.get("meal_plan", {}) if isinstance(diet_plan, dict) else {}
    workout_days = list((fitness_plan.get("detailed_plan", {}) if isinstance(fitness_plan, dict) else {}).keys())
    goal_key = str(profile.get("goal") or diet_plan.get("goal") or plan_doc.get("goal") or "maintenance").lower()
    goal = goal_key.replace("_", " ")
    diet_type = str(profile.get("dietType") or diet_plan.get("diet_preference") or plan_doc.get("diet_type") or "veg")

    current_weight = weight_context.get("current_weight")
    target_weight = weight_context.get("target_weight")
    weight_gap = None
    if current_weight is not None and target_weight is not None:
        weight_gap = round(current_weight - target_weight, 1)

    if _contains_abusive_language(message):
        return {
            "assistant_message": "I can help with diet, training, and goal planning, but I can’t continue when the message is abusive. Rephrase it respectfully and I’ll give you the best possible answer.",
            "quick_actions": [
                "Make me a diet plan for fat loss",
                "How much protein do I need?",
                "What workout should I follow this week?",
            ],
            "reminder_suggestion": "Reopen the coach with a respectful question and I’ll build your plan.",
            "starter_prompt": "I want a personalized diet and workout strategy based on my current weight and target weight.",
            "coach_strategy": {
                "goal": goal,
                "current_weight": current_weight,
                "target_weight": target_weight,
                "weekly_focus": ["Respectful re-entry required"],
                "meal_rules": ["Use respectful language to continue"],
                "workout_rules": ["Use respectful language to continue"],
                "check_in": "Rephrase your question and I’ll help you right away.",
            },
            "coach_summary": {
                "goal": goal,
                "calories": calories if 'calories' in locals() else 0,
                "protein": protein if 'protein' in locals() else 0,
                "carbs": carb if 'carb' in locals() else 0,
                "fats": fat if 'fat' in locals() else 0,
                "meal_plan_summary": _summarize_meal_plan(diet_plan),
                "workout_days": workout_days,
                "current_weight": current_weight,
                "target_weight": target_weight,
                "weight_gap": weight_gap,
                "reminder_suggestion": "Rephrase your question and I’ll help you right away.",
                "starter_prompt": "I want a personalized diet and workout strategy based on my current weight and target weight.",
            },
        }

    opening_parts = [f"I’ve tailored this for your {goal} plan with a {diet_type} preference."]
    if current_weight is not None and target_weight is not None:
        if weight_gap is not None and weight_gap > 0:
            opening_parts.append(f"You’re aiming to move from {current_weight:g} kg to {target_weight:g} kg, so the focus is steady fat loss without crashing energy.")
        elif weight_gap is not None and weight_gap < 0:
            opening_parts.append(f"You want to move from {current_weight:g} kg to {target_weight:g} kg, so the plan should support controlled gain with better training fuel.")
        else:
            opening_parts.append(f"Your current and target weight look matched, so I’ll keep the plan balanced and sustainable.")
    opening = " ".join(opening_parts)

    calories = daily_macros.get("calories") or diet_plan.get("daily_targets", {}).get("calories") or 0
    protein = daily_macros.get("protein") or diet_plan.get("daily_targets", {}).get("protein") or 0
    carb = daily_macros.get("carbs") or diet_plan.get("daily_targets", {}).get("carbs") or 0
    fat = daily_macros.get("fats") or daily_macros.get("fat") or diet_plan.get("daily_targets", {}).get("fat") or 0

    if current_weight is not None and target_weight is not None and goal_key == "weight_loss":
        gap = max(0.0, current_weight - target_weight)
        calories = max(1200, int(calories or round(current_weight * 22)) - min(500, int(gap * 25)))
        protein = max(int(protein or 0), int(round(target_weight * 1.7)))
        carb = max(0, int(round(calories * 0.4 / 4)))
        fat = max(0, int(round(calories * 0.25 / 9)))
    elif current_weight is not None and target_weight is not None and goal_key == "muscle_gain":
        calories = max(int(calories or round(current_weight * 28)), int(round(current_weight * 28)) + 200)
        protein = max(int(protein or 0), int(round(target_weight * 1.8)))

    safety_warning = _safety_warning(message, current_weight, target_weight, goal_key)
    opening_parts = [f"I’ve tailored this for your {goal} plan with a {diet_type} preference."]

    meal_focus = ""
    selected_meal_key = None
    lowered = message.lower()
    for key in ["breakfast", "lunch", "dinner", "snack", "evening"]:
        if key in lowered and key in meal_plan:
            selected_meal_key = key
            break

    if not selected_meal_key and meal_plan:
        selected_meal_key = next(iter(meal_plan.keys()))

    selected_meal = meal_plan.get(selected_meal_key, {}) if selected_meal_key else {}
    selected_breakdown = selected_meal.get("breakdown", {}) if isinstance(selected_meal, dict) else {}

    if focus == "meal":
        meal_focus = (
            f"For your next meal, use {selected_breakdown.get('name', 'a balanced meal')} and keep the plate close to your target macros. "
            f"Aim around {calories} kcal/day overall, with roughly {protein}g protein, {carb}g carbs, and {fat}g fats."
        )
    elif focus == "protein":
        meal_focus = (
            f"Protein is your anchor right now. Your target is about {protein}g per day, so prioritize paneer, eggs, dal, yogurt, chicken, or soy in each meal."
        )
    elif focus == "calorie":
        meal_focus = (
            f"Your calorie target is around {calories} kcal/day. If you want faster fat loss, tighten portions and keep snacks protein-heavy; if you want muscle gain, add a little more rice, roti, oats, or healthy fats."
        )
    elif focus == "workout":
        next_day = workout_days[0] if workout_days else "your next training day"
        meal_focus = (
            f"For {next_day}, keep a carb-containing meal 60 to 90 minutes before training and a protein-focused meal after."
        )
    elif focus == "recovery":
        meal_focus = (
            "Recovery matters as much as training. Keep water intake steady, sleep on time, and avoid making the last meal too heavy if you train late."
        )
    else:
        meal_focus = (
            f"A simple rule for today: stay close to {calories} kcal, hit your protein target, and use the meal plan instead of guessing portions."
        )

    if selected_meal_key and selected_breakdown:
        meal_focus += (
            f" Your {selected_meal_key} option is {selected_breakdown.get('name', 'a planned meal')} "
            f"with about {selected_breakdown.get('macros', {}).get('calories', 0)} kcal and {selected_breakdown.get('macros', {}).get('protein', 0)}g protein."
        )

    strategy = _build_strategy_lines(goal_key, focus, {"calories": calories, "protein": protein, "carbs": carb, "fats": fat}, workout_days, weight_context)

    strategy_meal_line = f"Keep your meals close to {strategy['calorie_target']} kcal and {strategy['protein_target']}g protein."
    if strategy.get("weight_gap") is not None and strategy["weight_gap"] > 0:
        strategy_meal_line = f"You need to lose about {strategy['weight_gap']} kg, so the best move is a steady deficit, not extreme restriction."
    elif strategy.get("weight_gap") is not None and strategy["weight_gap"] < 0:
        strategy_meal_line = f"You need to gain about {abs(strategy['weight_gap'])} kg, so add fuel around workouts instead of random snacking."

    history_note = ""
    if history:
      recent_user_turns = [item.get("content", "") for item in history if item.get("role") == "user"][-2:]
      if recent_user_turns:
          history_note = f"I also remember your recent focus on: {', '.join(recent_user_turns)}."

    reply_sections = [
        opening,
        f"Direct answer: {meal_focus}",
        f"Diet strategy: {strategy_meal_line}",
        f"Workout strategy: {', '.join(strategy['workout_rules'][:3])}.",
    ]
    if safety_warning:
        reply_sections.append(f"Safety note: {safety_warning}")
    reply_sections.extend([
        history_note,
        f"Next check-in: {strategy['check_in']}",
        f"Follow-up: {_clarifying_question(focus, current_weight, target_weight, goal)}",
    ])

    reply = "\n\n".join(part for part in reply_sections if part).strip()

    suggestions = [
        "What should I eat before training?",
        "How do I increase protein without overspending?",
        "What should I change for faster fat loss?",
        "What is my next workout focus?",
    ]

    if focus == "meal":
        suggestions = [
            "Show me a cheap high-protein meal idea",
            "What should I eat after workout?",
            "Which meal should I swap today?",
        ]
    elif focus == "workout":
        suggestions = [
            "What should I eat before training?",
            "What should I eat after training?",
            "How many calories should I burn?",
        ]

    if current_weight is not None and target_weight is not None and goal_key == "weight_loss":
        suggestions = [
            "Show me a 93 kg to 80 kg fat-loss strategy",
            "What meals keep me full while cutting calories?",
            "What workout split should I follow this week?",
        ]

    if safety_warning:
        suggestions = [
            "Give me a safer target",
            "How fast should I lose weight?",
            "What is the best calorie deficit for me?",
        ]

    reminder_suggestion = strategy["check_in"]
    starter_prompt = (
        f"I am {current_weight:g} kg and want to reach {target_weight:g} kg. Build a diet, workout, and check-in strategy for me."
        if current_weight is not None and target_weight is not None
        else f"Build me a personalized {goal} diet and workout strategy using my current plan."
    )

    return {
        "assistant_message": reply,
        "quick_actions": suggestions,
        "reminder_suggestion": reminder_suggestion,
        "starter_prompt": starter_prompt,
        "coach_strategy": strategy,
        "answer_mode": "safety" if safety_warning else "personalized",
        "needs_clarification": current_weight is None or target_weight is None,
        "coach_summary": {
            "goal": goal,
            "calories": calories,
            "protein": protein,
            "carbs": carb,
            "fats": fat,
            "meal_plan_summary": _summarize_meal_plan(diet_plan),
            "workout_days": workout_days,
            "current_weight": current_weight,
            "target_weight": target_weight,
            "weight_gap": strategy.get("weight_gap"),
            "reminder_suggestion": reminder_suggestion,
            "starter_prompt": starter_prompt,
        },
    }


def _save_coach_turn(email: str, role: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
    normalized_email = _normalize_email(email)
    if not normalized_email:
        return

    db = get_database()
    db["coach_messages"].insert_one(
        {
            "email": normalized_email,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc),
        }
    )


@router.get("/ml/personal-coach/{email}/history")
def get_personal_coach_history(email: str, limit: int = 12) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    bounded_limit = max(1, min(limit, 50))
    history = _recent_coach_history(normalized_email, bounded_limit)

    return {
        "status": "success",
        "email": normalized_email,
        "count": len(history),
        "messages": [
            {
                "id": str(item.get("_id")),
                "role": item.get("role", "assistant"),
                "content": item.get("content", ""),
                "metadata": item.get("metadata", {}),
                "created_at": item.get("created_at"),
            }
            for item in history
        ],
    }


@router.post("/ml/personal-coach/{email}")
def ask_personal_coach(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    message = str(data.get("message", "")).strip()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="email is required")
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    user_profile = data.get("user_profile", {}) if isinstance(data.get("user_profile", {}), dict) else {}
    plan_doc = data.get("current_plan", {}) if isinstance(data.get("current_plan", {}), dict) else {}
    if not plan_doc:
        plan_doc = _latest_plan_for_email(normalized_email)

    history = _recent_coach_history(normalized_email)
    _save_coach_turn(normalized_email, "user", message, {"source": "frontend"})

    coach_response = _build_coach_reply(normalized_email, message, user_profile, plan_doc, history)
    assistant_message = coach_response["assistant_message"]

    _persist_coach_memory(normalized_email, user_profile, coach_response.get("coach_strategy", {}), _extract_focus(message))

    _save_coach_turn(
        normalized_email,
        "assistant",
        assistant_message,
        {"quick_actions": coach_response.get("quick_actions", []), "coach_summary": coach_response.get("coach_summary", {})},
    )

    reminder_suggestion = str(coach_response.get("reminder_suggestion") or "").strip()
    if reminder_suggestion:
        create_user_notification(
            normalized_email,
            "Coach follow-up ready",
            reminder_suggestion,
            notification_type="reminder",
            action_label="Open Coach",
            action_path="/result",
            source="coach",
            priority="normal",
        )

    return {
        "status": "success",
        "email": normalized_email,
        **coach_response,
    }


@router.post("/ml/food-recognition")
def recognize_food_from_image(data: Dict[str, Any]) -> Dict[str, Any]:
    image_path = data.get("image_path", "")
    if not image_path:
        raise HTTPException(status_code=400, detail="image_path or image_base64 required")
    return food_recognition_service.recognize_food_from_image(image_path)


@router.post("/ml/nutrition-from-text")
def predict_nutrition_from_text(data: Dict[str, Any]) -> Dict[str, Any]:
    description = str(data.get("food_description", "")).strip()
    if not description:
        raise HTTPException(status_code=400, detail="food_description required")
    return food_recognition_service.predict_nutrition_from_text(description)


@router.post("/ml/daily-macros/{email}")
def predict_daily_macros(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    user_profile = {
        "email": email,
        "weight": float(data.get("weight", 70)),
        "age": int(data.get("age", 25)),
        "fitness_level": str(data.get("fitness_level", "moderate")).lower(),
        "goal": str(data.get("goal", "maintenance")).lower(),
    }

    result = nutrition_prediction_service.predict_daily_macros(user_profile)
    return {
        "status": "success",
        "email": email,
        "macro_recommendation": result,
    }


@router.get("/ml/meal-timing/{email}")
def get_optimal_meal_timing(email: str, workout_time: str = None) -> Dict[str, Any]:
    timing = nutrition_prediction_service.predict_meal_timing({}, workout_time)
    return {
        "status": "success",
        "email": email,
        "meal_timing": timing,
    }


@router.post("/ml/personalized-exercises/{email}")
def get_personalized_exercises(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    user_prefs = {
        "goal": str(data.get("goal", "maintenance")).lower(),
        "prefer_compound": bool(data.get("prefer_compound", False)),
        "fitness_level": str(data.get("fitness_level", "moderate")).lower(),
        "difficulty_preference": str(data.get("difficulty_preference", data.get("fitness_level", "moderate"))).lower(),
        "preferred_muscle_groups": data.get("preferred_muscle_groups", []),
        "equipment_access": data.get("equipment_access", []),
        "injury_notes": data.get("injury_notes", []),
        "injury_history": data.get("injury_history", []),
        "avoid_exercises": data.get("avoid_exercises", []),
        "disliked_exercises": data.get("disliked_exercises", []),
    }

    recommendations = exercise_personalization_service.personalize_exercise_plan(email, user_prefs, [])
    return {
        "status": "success",
        "email": email,
        "recommended_exercises": recommendations,
        "note": "Recommendations improve with more performance history",
    }


@router.post("/ml/predict-difficulty/{email}")
def predict_workout_difficulty(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    exercises = data.get("exercise_ids", [])
    difficulty = exercise_personalization_service.predict_workout_difficulty(email, exercises)
    return {
        "status": "success",
        "email": email,
        **difficulty,
    }


@router.post("/ml/goal-achievement/{email}")
def predict_goal_achievement(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    goal = str(data.get("goal", "weight_loss")).lower()
    adherence = data.get("adherence_history", [])
    prediction = goal_achievement_service.predict_goal_achievement(email, goal, adherence)
    return {
        "status": "success",
        "email": email,
        **prediction,
    }


@router.post("/ml/timeline-to-goal/{email}")
def estimate_goal_timeline(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    current = float(data.get("current_weight", 70))
    goal = float(data.get("goal_weight", 65))
    adherence = float(data.get("weekly_adherence", 0.8))
    timeline = goal_achievement_service.predict_timeline_to_goal(current, goal, adherence)
    return {
        "status": "success",
        "email": email,
        **timeline,
    }


@router.post("/ml/optimize-meal-plan/{email}")
def optimize_meal_plan(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    current_meals = data.get("current_meals", {})
    feedback = data.get("feedback", [])
    optimization = meal_optimization_service.optimize_meal_plan(email, current_meals, feedback)
    return {
        "status": "success",
        "email": email,
        "optimizations": optimization,
    }


@router.post("/ml/predict-meal-adherence/{email}")
def predict_meal_adherence(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    meal = str(data.get("proposed_meal", "")).strip()
    history = data.get("user_history", [])
    adherence = meal_optimization_service.predict_meal_adherence(email, meal, history)
    return {
        "status": "success",
        "email": email,
        "proposed_meal": meal,
        "predicted_adherence_score": adherence,
        "note": f"{'High' if adherence > 0.7 else 'Medium' if adherence > 0.5 else 'Low'} likelihood of adherence",
    }


@router.post("/ml/strength-progression/{email}/{exercise_id}")
def predict_strength_progression(email: str, exercise_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    history = data.get("performance_history", [])
    prediction = performance_tracking_service.predict_strength_progression(email, exercise_id, history)
    return {
        "status": "success",
        "email": email,
        "exercise_id": exercise_id,
        **prediction,
    }


@router.post("/ml/recovery-recommendations/{email}")
def get_recovery_recommendations(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    workouts = data.get("recent_workouts", [])
    recommendations = performance_tracking_service.predict_recovery_needs(email, workouts)
    return {
        "status": "success",
        "email": email,
        **recommendations,
    }


@router.post("/ml/comprehensive-recommendations/{email}")
def get_comprehensive_ml_recommendations(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    performance_history = data.get("performance_history", [])
    user_profile = {
        "email": email,
        "weight": float(data.get("weight", 70)),
        "age": int(data.get("age", 25)),
        "fitness_level": str(data.get("fitness_level", "moderate")).lower(),
        "goal": str(data.get("goal", "maintenance")).lower(),
        "preferred_muscle_groups": data.get("preferred_muscle_groups", []),
        "injury_notes": data.get("injury_notes", []),
        "injury_history": data.get("injury_history", []),
        "avoid_exercises": data.get("avoid_exercises", []),
        "disliked_exercises": data.get("disliked_exercises", []),
        "equipment_access": data.get("equipment_access", []),
        "difficulty_preference": str(data.get("difficulty_preference", data.get("fitness_level", "moderate"))).lower(),
        "prefer_compound": bool(data.get("prefer_compound", False)),
        "performance_history": performance_history,
    }

    recommendations = ml_pipeline_service.get_personalized_recommendations(email, user_profile)

    return {
        **recommendations,
        "profile_summary": {
            "fitness_level": user_profile["fitness_level"],
            "goal": user_profile["goal"],
            "equipment_access": user_profile["equipment_access"],
            "injury_notes": user_profile["injury_notes"],
            "preferred_muscle_groups": user_profile["preferred_muscle_groups"],
        },
    }
