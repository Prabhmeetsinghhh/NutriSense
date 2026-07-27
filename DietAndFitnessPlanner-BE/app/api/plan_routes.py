from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.config import APP_ENV
from app.db.mongo import get_database, get_database_mode
from app.models.exercises import EXERCISES_DATABASE, MUSCLE_GROUPS
from app.api.notification_routes import create_user_notification
from app.services.dietService import IndianDietService
from app.services.fitnessService import get_fitness_plan
from app.services.mlService import get_ml_runtime_status

router = APIRouter()


def _save_plan_to_db(user_input: Dict[str, Any], response_payload: Dict[str, Any]) -> str:
    db = get_database()
    users = db["users"]
    plans = db["plan_history"]

    now = datetime.now(timezone.utc)
    email = str(user_input.get("email", "")).strip().lower()

    if email:
        users.update_one(
            {"email": email},
            {
                "$set": {
                    "name": user_input.get("name", "User"),
                    "age": user_input.get("age"),
                    "weight": user_input.get("weight"),
                    "target_weight": user_input.get("targetWeight") or user_input.get("target_weight"),
                    "heightFeet": user_input.get("heightFeet"),
                    "heightInches": user_input.get("heightInches"),
                    "fitnessLevel": user_input.get("fitnessLevel"),
                    "goal": user_input.get("goal"),
                    "dietType": user_input.get("dietType"),
                    "budget_preference": user_input.get("budget_preference"),
                    "injury_notes": user_input.get("injury_notes"),
                    "avoid_exercises": user_input.get("avoid_exercises"),
                    "equipment_access": user_input.get("equipment_access"),
                    "updated_at": now,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )

    plan_doc = {
        "email": email,
        "name": response_payload.get("user_name", "User"),
        "goal": response_payload.get("diet_plan", {}).get("goal"),
        "fitness_level": response_payload.get("diet_plan", {}).get("experience"),
        "diet_type": response_payload.get("diet_plan", {}).get("diet_preference"),
        "budget_preference": user_input.get("budget_preference"),
        "target_weight": user_input.get("targetWeight") or user_input.get("target_weight"),
        "diet_plan": response_payload.get("diet_plan"),
        "fitness_plan": response_payload.get("fitness_plan"),
        "status": response_payload.get("status", "success"),
        "message": response_payload.get("message"),
        "created_at": now,
    }

    inserted = plans.insert_one(plan_doc)
    return str(inserted.inserted_id)


def _to_float_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int_or_none(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _validate_feedback_payload(payload: Dict[str, Any]) -> tuple[bool, str]:
    plan_id = str(payload.get("plan_id", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    adherence_percent = _to_int_or_none(payload.get("adherence_percent"))
    energy_rating = _to_int_or_none(payload.get("energy_rating"))
    hunger_rating = _to_int_or_none(payload.get("hunger_rating"))
    sleep_hours = _to_float_or_none(payload.get("sleep_hours"))

    if not plan_id:
        return False, "plan_id is required"
    if not email:
        return False, "email is required"
    if adherence_percent is None or adherence_percent < 0 or adherence_percent > 100:
        return False, "adherence_percent must be between 0 and 100"
    if energy_rating is not None and (energy_rating < 1 or energy_rating > 5):
        return False, "energy_rating must be between 1 and 5"
    if hunger_rating is not None and (hunger_rating < 1 or hunger_rating > 5):
        return False, "hunger_rating must be between 1 and 5"
    if sleep_hours is not None and (sleep_hours < 0 or sleep_hours > 24):
        return False, "sleep_hours must be between 0 and 24"

    return True, ""


def parse_exercise_string(exercise_str: str) -> dict:
    exercise_data = {
        "name": exercise_str,
        "sets": None,
        "reps": None,
        "duration": None,
    }

    sets_match = __import__("re").search(r"(\d+)\s*sets?\s*x\s*(\d+(?:-\d+)?)\s*reps?", exercise_str, __import__("re").IGNORECASE)
    if sets_match:
        exercise_data["sets"] = int(sets_match.group(1))
        exercise_data["reps"] = sets_match.group(2)
        exercise_data["name"] = __import__("re").sub(r"\s*\(\d+\s*sets?\s*x\s*[\d\-]+\s*reps?\)", "", exercise_str).strip()

    duration_match = __import__("re").search(r"(\d+(?:-\d+)?)\s*mins?", exercise_str, __import__("re").IGNORECASE)
    if duration_match:
        exercise_data["duration"] = duration_match.group(1) + " mins"
        exercise_data["name"] = __import__("re").sub(r"\s*\d+(?:-\d+)?\s*mins?", "", exercise_data["name"]).strip()

    return exercise_data


def _parse_cost_mid(cost_str: str) -> float:
    cleaned = str(cost_str).replace("₹", "").replace("Rs.", "").strip()
    if "-" in cleaned:
        parts = [p.strip() for p in cleaned.split("-") if p.strip()]
        nums = [float(p) for p in parts]
        return sum(nums) / len(nums) if nums else 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_cost_range(cost_str: str) -> Dict[str, float]:
    cleaned = str(cost_str).replace("₹", "").replace("Rs.", "").strip()
    if "-" in cleaned:
        parts = [p.strip() for p in cleaned.split("-") if p.strip()]
        nums = [float(p) for p in parts]
        if len(nums) == 2:
            return {"min": nums[0], "max": nums[1]}
        if len(nums) == 1:
            return {"min": nums[0], "max": nums[0]}
        return {"min": 0.0, "max": 0.0}
    try:
        num = float(cleaned)
        return {"min": num, "max": num}
    except ValueError:
        return {"min": 0.0, "max": 0.0}


def _goal_context(goal: str) -> Dict[str, str]:
    context = {
        "muscle_gain": {
            "energy": "calorie surplus to support muscle growth",
            "priority": "high protein + consistent carbs",
        },
        "weight_loss": {
            "energy": "calorie deficit while preserving muscle",
            "priority": "high satiety protein + controlled carbs",
        },
        "maintenance": {
            "energy": "balanced intake for stable weight",
            "priority": "steady macros and routine",
        },
        "muscle_endurance": {
            "energy": "high-work output fueling",
            "priority": "quality carbs + adequate protein",
        },
    }
    return context.get(goal, context["maintenance"])


def _meal_explanation(meal_time: str, goal: str, meal_info: Dict[str, Any]) -> Dict[str, str]:
    context = _goal_context(goal)
    calories = meal_info.get("calories", 0)
    protein = meal_info.get("protein", 0)
    carbs = meal_info.get("carbs", meal_info.get("macros", {}).get("carbs", 0))

    timing_map = {
        "breakfast": "Breakfast helps restore glycogen after overnight fasting and sets appetite control for the day.",
        "lunch": "Lunch is your central fueling window to maintain training performance and stable focus.",
        "snack": "Evening snack prevents long gaps and protects muscle by keeping protein pulses consistent.",
        "evening": "Evening snack prevents long gaps and protects muscle by keeping protein pulses consistent.",
        "dinner": "Dinner supports overnight recovery and should close your macro targets without heavy overeating.",
    }

    benefit_map = {
        "breakfast": f"This meal gives around {calories} kcal with {protein}g protein and {carbs}g carbs to start recovery and energy availability early.",
        "lunch": f"This meal anchors your day with around {calories} kcal and strong macro coverage for {context['priority']}.",
        "snack": f"This meal stabilizes hunger and performance with around {calories} kcal while supporting {context['energy']}.",
        "evening": f"This meal stabilizes hunger and performance with around {calories} kcal while supporting {context['energy']}.",
        "dinner": f"This meal closes the day to match your {context['energy']} target and improves next-day readiness.",
    }

    return {
        "why_this_meal": benefit_map.get(meal_time, benefit_map["lunch"]),
        "why_now": timing_map.get(meal_time, timing_map["lunch"]),
        "goal_alignment": f"Chosen for {goal.replace('_', ' ')} with focus on {context['priority']}.",
    }


def _itemized_costs(portion_text: str, meal_cost: str) -> list[dict[str, Any]]:
    parts = [p.strip() for p in str(portion_text).split(",") if p.strip()]
    if not parts:
        return []
    parsed = _parse_cost_range(meal_cost)

    base_weights = {
        "egg": 1.3,
        "bread": 0.8,
        "roti": 0.9,
        "rice": 1.0,
        "dal": 1.4,
        "paneer": 2.0,
        "chicken": 2.4,
        "fish": 2.3,
        "milk": 1.2,
        "curd": 1.1,
        "oats": 1.2,
        "peanut butter": 1.5,
        "peanuts": 1.0,
        "banana": 0.8,
        "fruit": 0.9,
        "chai": 0.7,
        "tea": 0.7,
        "coffee": 0.8,
        "soya": 1.6,
        "sabzi": 1.1,
        "vegetables": 1.1,
    }

    def _weight_for_item(item_text: str) -> float:
        text = item_text.lower()
        qty = 1.0
        qty_match = __import__("re").search(r"(\d+(?:\.\d+)?)", text)
        if qty_match:
            try:
                parsed_qty = float(qty_match.group(1))
                qty = max(0.6, min(parsed_qty, 4.0))
            except ValueError:
                qty = 1.0

        best = 1.0
        for key, val in base_weights.items():
            if key in text:
                best = val
                break
        return best * qty

    weights = [_weight_for_item(item) for item in parts]
    total_weight = sum(weights) if sum(weights) > 0 else float(len(parts))

    rows = []
    for item, weight in zip(parts, weights):
        share = weight / total_weight
        unit_min = round(parsed["min"] * share)
        unit_max = round(parsed["max"] * share)
        rows.append(
            {
                "item": item,
                "estimated_cost": f"₹{unit_min}-{unit_max}" if unit_min != unit_max else f"₹{unit_min}",
            }
        )
    return rows


@router.get("/health")
def health() -> Dict[str, Any]:
    db = get_database()
    db.command("ping")
    return {
        "status": "ok",
        "environment": APP_ENV,
        "database": db.name,
        "database_mode": get_database_mode(),
        "persistent_storage": get_database_mode() == "mongodb",
        "ml_runtime": get_ml_runtime_status(),
    }


@router.get("/health/db")
def health_db() -> dict:
    try:
        db = get_database()
        db.command("ping")
        return {
            "status": "ok",
            "database": db.name,
            "mode": get_database_mode(),
            "persistent_storage": get_database_mode() == "mongodb",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {exc}") from exc


@router.get("/plans/{email}")
def get_user_plan_history(email: str, limit: int = 10) -> dict:
    normalized_email = email.strip().lower()
    bounded_limit = max(1, min(limit, 50))

    db = get_database()
    cursor = (
        db["plan_history"]
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(bounded_limit)
    )

    plans = []
    for row in cursor:
        plans.append(
            {
                "id": str(row.get("_id")),
                "email": row.get("email"),
                "name": row.get("name"),
                "goal": row.get("goal"),
                "fitness_level": row.get("fitness_level"),
                "diet_type": row.get("diet_type"),
                "budget_preference": row.get("budget_preference"),
                "created_at": row.get("created_at"),
            }
        )

    return {
        "status": "success",
        "email": normalized_email,
        "count": len(plans),
        "plans": plans,
    }


@router.post("/plan-feedback")
def submit_plan_feedback(data: Dict[str, Any]) -> Dict[str, Any]:
    ok, error_message = _validate_feedback_payload(data)
    if not ok:
        raise HTTPException(status_code=400, detail=error_message)

    db = get_database()
    feedback_collection = db["plan_feedback"]
    users = db["users"]

    now = datetime.now(timezone.utc)
    email = str(data.get("email", "")).strip().lower()
    plan_id = str(data.get("plan_id", "")).strip()

    feedback_doc = {
        "plan_id": plan_id,
        "email": email,
        "adherence_percent": _to_int_or_none(data.get("adherence_percent")),
        "weight_now": _to_float_or_none(data.get("weight_now")),
        "energy_rating": _to_int_or_none(data.get("energy_rating")),
        "hunger_rating": _to_int_or_none(data.get("hunger_rating")),
        "sleep_hours": _to_float_or_none(data.get("sleep_hours")),
        "feedback_text": str(data.get("feedback_text", "")).strip(),
        "created_at": now,
    }

    inserted = feedback_collection.insert_one(feedback_doc)

    users.update_one(
        {"email": email},
        {
            "$set": {
                "updated_at": now,
                "last_feedback_at": now,
            }
        },
        upsert=True,
    )

    return {
        "status": "success",
        "message": "Feedback saved",
        "feedback_id": str(inserted.inserted_id),
    }


@router.get("/plan-feedback/{email}")
def get_plan_feedback(email: str, limit: int = 20) -> Dict[str, Any]:
    normalized_email = email.strip().lower()
    bounded_limit = max(1, min(limit, 100))

    db = get_database()
    cursor = (
        db["plan_feedback"]
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(bounded_limit)
    )

    rows = []
    for row in cursor:
        rows.append(
            {
                "id": str(row.get("_id")),
                "plan_id": row.get("plan_id"),
                "email": row.get("email"),
                "adherence_percent": row.get("adherence_percent"),
                "weight_now": row.get("weight_now"),
                "energy_rating": row.get("energy_rating"),
                "hunger_rating": row.get("hunger_rating"),
                "sleep_hours": row.get("sleep_hours"),
                "feedback_text": row.get("feedback_text"),
                "created_at": row.get("created_at"),
            }
        )

    return {
        "status": "success",
        "email": normalized_email,
        "count": len(rows),
        "feedback": rows,
    }


@router.post("/generate-plan")
def generate_plan(data: dict):
    """
    Generate personalized Indian diet and fitness plan
    Expected fields: name, email, age, heightFeet, heightInches, weight,
                     fitnessLevel, goal, dietType, budget_preference, injury_notes, avoid_exercises, equipment_access
    """
    try:
        name = data.get("name", "User")
        age = int(data.get("age", 25))
        weight = int(data.get("weight", 70))
        height_feet = int(data.get("heightFeet", 5))
        height_inches = int(data.get("heightInches", 10))
        height_cm = (height_feet * 30.48) + (height_inches * 2.54)

        goal = data.get("goal", "maintenance")
        fitness_level = data.get("fitnessLevel", "intermediate")
        budget_preference = data.get("budget_preference", "value")
        diet_type = data.get("dietType", "veg")
        injury_notes = str(data.get("injury_notes", "")).strip()
        avoid_exercises = data.get("avoid_exercises", [])
        equipment_access = data.get("equipment_access", [])

        goal_mapping = {
            "muscle_gain": "muscle_gain",
            "weight_loss": "weight_loss",
            "fat_loss": "weight_loss",
            "maintenance": "maintenance",
            "muscle_endurance": "muscle_endurance",
            "gain": "muscle_gain",
            "loss": "weight_loss",
            "maintain": "maintenance",
            "endurance": "muscle_endurance",
        }
        goal = goal_mapping.get(goal.lower(), "maintenance")

        diet_fitness_level_mapping = {
            "amateur": "light",
            "beginner": "light",
            "intermediate": "moderate",
            "professional": "active",
            "advanced": "active",
            "athlete": "very_active",
            "sedentary": "sedentary",
            "light": "light",
            "moderate": "moderate",
            "active": "active",
            "very_active": "very_active",
        }
        diet_fitness_level = diet_fitness_level_mapping.get(fitness_level.lower(), "moderate")

        diet_preference_mapping = {
            "veg": "veg",
            "non_veg": "non_veg",
            "vegan": "vegan",
            "eggetarian": "veg_egg",
            "veg_egg": "veg_egg",
        }
        diet_preference = diet_preference_mapping.get(diet_type.lower(), "veg")

        diet_plan_raw = IndianDietService.generate_indian_meal_plan(
            name=name,
            age=age,
            weight=weight,
            height_cm=height_cm,
            fitness_level=diet_fitness_level,
            goal=goal,
            budget_preference=budget_preference,
            diet_type=diet_preference,
        )

        bmi = round(IndianDietService.calculate_bmi(weight, height_cm), 1)

        fitness_plan_raw = get_fitness_plan(
            age,
            weight,
            fitness_level,
            goal,
            {
                "injury_notes": injury_notes,
                "avoid_exercises": avoid_exercises,
                "equipment_access": equipment_access,
            },
        )

        diet_plan = {
            "daily_macros": {
                "calories": diet_plan_raw["daily_targets"]["calories"],
                "protein": diet_plan_raw["daily_targets"]["protein"],
                "carbs": diet_plan_raw["daily_targets"]["carbs"],
                "fats": diet_plan_raw["daily_targets"]["fat"],
            },
            "meal_plan": {},
            "diet_tips": diet_plan_raw["diet_tips"],
            "hydration": diet_plan_raw["hydration"],
            "budget_tier": diet_plan_raw["budget_tier"],
            "daily_totals": diet_plan_raw["daily_totals"],
            "bmi": bmi,
            "goal": goal,
            "experience": fitness_level,
            "diet_preference": diet_preference,
            "daily_budget_hint": diet_plan_raw["budget_tier"]["name"],
        }

        estimated_daily_cost = 0.0
        estimated_daily_min = 0.0
        estimated_daily_max = 0.0
        for meal_time, meal_info in diet_plan_raw["daily_plan"].items():
            display_meal_time = "evening" if meal_time == "snack" else meal_time
            meal_calories = meal_info.get("calories", 0)
            meal_protein = meal_info.get("protein", 0)
            meal_carbs = meal_info.get("carbs", meal_info.get("macros", {}).get("carbs", 0))
            meal_fat = meal_info.get("fat", meal_info.get("macros", {}).get("fat", 0))
            meal_cost = meal_info.get("cost", "₹0")
            estimated_daily_cost += _parse_cost_mid(meal_cost)
            cost_range = _parse_cost_range(meal_cost)
            estimated_daily_min += cost_range["min"]
            estimated_daily_max += cost_range["max"]
            explanation = _meal_explanation(display_meal_time, goal, meal_info)
            cost_breakdown = _itemized_costs(meal_info.get("portion", ""), meal_cost)

            overview = f"{meal_info.get('name', 'Meal')} ({meal_info.get('portion', '')}) - {meal_cost}"

            breakdown = {
                "name": meal_info.get("name", ""),
                "portion": meal_info.get("portion", ""),
                "macros": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat,
                },
                "cost": meal_cost,
                "prep_time": meal_info.get("prep_time", ""),
                "availability": meal_info.get("availability", ""),
                "protein_booster": meal_info.get("protein_booster"),
                "explanation": explanation,
                "itemized_costs": cost_breakdown,
            }

            diet_plan["meal_plan"][display_meal_time] = {
                "overview": overview,
                "breakdown": breakdown,
            }

            diet_plan["estimated_daily_cost"] = round(estimated_daily_cost, 1)
        diet_plan["estimated_daily_cost_range"] = {
            "min": round(estimated_daily_min, 1),
            "max": round(estimated_daily_max, 1),
        }
        diet_plan["spend_strategy"] = (
            "Cost values are per-meal estimates based on selected tier and common Indian serving sizes. "
            "Item-level costs are split estimates to make budget planning easier."
        )

        detailed_plan = {}
        for day, workout_data in fitness_plan_raw["weekly_schedule"].items():
            parsed_exercises = [parse_exercise_string(ex) for ex in workout_data.get("exercises", [])]
            detailed_plan[day] = {
                "type": workout_data.get("focus", "Workout"),
                "exercises": parsed_exercises,
                "duration": workout_data.get("duration", ""),
                "recovery_tips": fitness_plan_raw.get("recovery_recommendations", [])[:3],
                "warmup": workout_data.get("warmup", []),
                "cooldown": workout_data.get("cooldown", []),
                "precautions": workout_data.get("precautions", []),
                "exercise_options": workout_data.get("exercise_options", []),
            }

        fitness_plan = {
            "user_info": {
                "age": age,
                "weight": weight,
                "fitness_level": fitness_level,
                "goal": goal,
                "injury_notes": injury_notes,
                "avoid_exercises": avoid_exercises,
                "equipment_access": equipment_access,
            },
            "detailed_plan": detailed_plan,
            "fitness_tips": fitness_plan_raw["fitness_tips"],
            "recovery_recommendations": fitness_plan_raw["recovery_recommendations"],
            "warmup_routine": fitness_plan_raw.get("warmup_routine", []),
            "cooldown_routine": fitness_plan_raw.get("cooldown_routine", []),
            "safety_notes": fitness_plan_raw.get("safety_notes", []),
            "exercise_swaps": fitness_plan_raw.get("exercise_swaps", []),
            "injury_context": fitness_plan_raw.get("injury_context", {}),
        }

        result_payload = {
            "status": "success",
            "user_name": name,
            "diet_plan": diet_plan,
            "fitness_plan": fitness_plan,
            "message": "आपकी व्यक्तिगत योजना तैयार हो गई है! 🎉",
        }

        persistence = {
            "saved": False,
            "plan_id": None,
            "error": None,
        }
        try:
            persistence["plan_id"] = _save_plan_to_db(data, result_payload)
            persistence["saved"] = True
            create_user_notification(
                data.get("email", ""),
                title="Your plan is ready",
                message="Your personalized diet and fitness plan has been saved. Open the result card to review it.",
                notification_type="success",
                action_label="Open plan",
                action_path="/result",
                source="plan_generation",
                priority="high",
            )
        except Exception as db_exc:
            persistence["error"] = str(db_exc)

        result_payload["persistence"] = persistence
        return result_payload
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Error generating plan: {str(e)}",
        }
