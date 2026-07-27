"""
Fitness Service - Generates personalized workout plans
"""

from __future__ import annotations

from typing import Any, Dict, List


INJURY_RULES = {
    "disc bulge": {
        "avoid": ["deadlift", "bent over row", "barbell row", "rows", "row", "good morning", "heavy squat", "romanian deadlift"],
        "substitutions": {
            "deadlift": "glute bridge",
            "bent over row": "chest supported row",
            "barbell row": "chest supported row",
            "rows": "chest supported row",
            "row": "chest supported row",
            "heavy squat": "goblet squat to box",
            "romanian deadlift": "bird dog",
        },
        "replace": [
            "glute bridge",
            "bird dog",
            "dead bug",
            "chest supported row",
            "lat pulldown",
            "goblet squat to box",
        ],
        "precautions": [
            "Keep a neutral spine and avoid loaded spinal flexion.",
            "Use supported rows instead of bent-over pulling patterns.",
            "Stop any movement that increases back pain or causes radiating symptoms.",
        ],
    },
    "lower back": {
        "avoid": ["deadlift", "bent over row", "rows", "row", "good morning", "hyperextension"],
        "substitutions": {
            "deadlift": "glute bridge",
            "bent over row": "chest supported row",
            "good morning": "dead bug",
            "hyperextension": "bird dog",
        },
        "replace": ["chest supported row", "lat pulldown", "glute bridge", "bird dog"],
        "precautions": [
            "Brace your core before each rep.",
            "Favor supported machines and split-stance patterns.",
        ],
    },
    "shoulder": {
        "avoid": ["shoulder press", "overhead press", "upright row", "lateral raise"],
        "substitutions": {
            "shoulder press": "landmine press",
            "overhead press": "landmine press",
            "upright row": "face pull",
            "lateral raise": "scapular wall slide",
        },
        "replace": ["landmine press", "incline push-up", "machine chest press", "face pull"],
        "precautions": [
            "Avoid painful overhead ranges until the shoulder is cleared.",
            "Use neutral-grip pressing and controlled tempo.",
        ],
    },
    "knee": {
        "avoid": ["jump squat", "burpee", "deep squat", "walking lunge"],
        "substitutions": {
            "jump squat": "step-up",
            "burpee": "incline push-up",
            "deep squat": "box squat",
            "walking lunge": "split squat to a comfortable depth",
        },
        "replace": ["step-up", "box squat", "glute bridge", "hamstring curl"],
        "precautions": [
            "Keep knee tracking over the toes without collapsing inward.",
            "Use a pain-free depth and slow eccentric control.",
        ],
    },
}


def get_fitness_plan(age: int, weight: int, fitness_level: str, goal: str, profile: Dict[str, Any] | None = None) -> dict:
    """
    Generate fitness plan based on user profile
    """
    
    # Map goal to workout type
    goal_mapping = {
        "muscle_gain": "strength",
        "weight_loss": "cardio_strength",
        "maintenance": "balanced",
        "muscle_endurance": "endurance",
        "gain": "strength",
        "loss": "cardio_strength",
        "maintain": "balanced",
        "endurance": "endurance",
    }
    
    workout_type = goal_mapping.get(goal.lower(), "balanced")
    
    # Fitness level-based intensity
    intensity_map = {
        "amateur": "beginner",
        "sedentary": "beginner",
        "light": "beginner",
        "intermediate": "intermediate",
        "moderate": "intermediate",
        "professional": "advanced",
        "advanced": "advanced",
        "active": "advanced",
        "very_active": "elite",
    }
    
    intensity = intensity_map.get(fitness_level.lower(), "intermediate")
    
    profile = profile or {}

    # Generate weekly plan
    weekly_schedule = generate_weekly_schedule(workout_type, intensity, age, weight, profile)

    injury_context = _build_injury_context(profile)
    warmup_routine = _build_warmup_routine(injury_context)
    cooldown_routine = _build_cooldown_routine(injury_context)
    
    return {
        "workout_type": workout_type,
        "intensity": intensity,
        "weekly_schedule": weekly_schedule,
        "fitness_tips": generate_fitness_tips(goal, fitness_level, age),
        "recovery_recommendations": generate_recovery_tips(intensity),
        "warmup_routine": warmup_routine,
        "cooldown_routine": cooldown_routine,
        "safety_notes": injury_context["precautions"],
        "exercise_swaps": injury_context["replacements"],
        "injury_context": injury_context,
    }


def _normalize_text_list(raw_value: Any) -> List[str]:
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        return [str(item).strip().lower() for item in raw_value if str(item).strip()]
    if isinstance(raw_value, str):
        return [part.strip().lower() for part in raw_value.replace("/", ",").split(",") if part.strip()]
    return [str(raw_value).strip().lower()]


def _build_injury_context(profile: Dict[str, Any]) -> Dict[str, Any]:
    injury_terms = _normalize_text_list(profile.get("injury_history"))
    injury_terms.extend(_normalize_text_list(profile.get("injury_notes")))
    injury_terms.extend(_normalize_text_list(profile.get("limitations")))

    avoid_exercises = _normalize_text_list(profile.get("avoid_exercises"))
    preferred_equipment = _normalize_text_list(profile.get("equipment_access"))

    precautions: List[str] = [
        "Warm up before every session and keep the first set light.",
        "Use pain as a stop signal, not something to push through.",
    ]
    replacements: List[str] = []
    avoid_patterns: List[str] = []
    substitutions: Dict[str, str] = {}

    for term in injury_terms:
        for key, rule in INJURY_RULES.items():
            if key in term:
                avoid_patterns.extend(rule["avoid"])
                replacements.extend(rule["replace"])
                substitutions.update(rule.get("substitutions", {}))
                precautions.extend(rule["precautions"])

    avoid_patterns.extend(avoid_exercises)
    replacements.extend(_safe_default_replacements(preferred_equipment))

    unique_precautions = list(dict.fromkeys(precautions))
    unique_replacements = list(dict.fromkeys(replacements))
    unique_avoid = list(dict.fromkeys(avoid_patterns))

    return {
        "injuries": injury_terms,
        "avoid_exercises": unique_avoid,
        "replacements": unique_replacements,
        "substitutions": substitutions,
        "precautions": unique_precautions,
        "equipment_access": preferred_equipment,
    }


def _safe_default_replacements(equipment_access: List[str]) -> List[str]:
    replacements = ["incline push-up", "step-up", "glute bridge", "bird dog", "dead bug", "walking"]
    if "barbell" in equipment_access:
        replacements.append("landmine press")
    if "dumbbells" in equipment_access:
        replacements.append("dumbbell floor press")
    if "pull_up_bar" in equipment_access or "pull up bar" in equipment_access:
        replacements.append("assisted pull-up")
    return replacements


def _build_warmup_routine(injury_context: Dict[str, Any]) -> List[str]:
    warmup = [
        "5 minutes easy walking or cycling",
        "Joint circles for shoulders, hips, knees, and ankles",
        "Dynamic mobility: arm swings, leg swings, torso rotations",
        "2 light ramp-up sets for the first main exercise",
    ]
    if injury_context["injuries"]:
        warmup.insert(1, "Gentle activation for the affected area before loading")
    return warmup


def _build_cooldown_routine(injury_context: Dict[str, Any]) -> List[str]:
    cooldown = [
        "3-5 minutes slow walking to lower heart rate",
        "Static stretching for the muscles trained today",
        "Breathing drill: 4 seconds in, 6 seconds out for 2 minutes",
    ]
    if injury_context["injuries"]:
        cooldown.append("Extra mobility work only in a pain-free range")
    return cooldown


def _apply_injury_modifications(exercises: List[str], injury_context: Dict[str, Any]) -> tuple[list[str], list[str]]:
    avoid_patterns = injury_context["avoid_exercises"]
    replacements = injury_context["replacements"]
    substitutions = injury_context.get("substitutions", {})
    modified_exercises: List[str] = []
    flagged: List[str] = []

    for exercise in exercises:
        lower_exercise = exercise.lower()
        if any(pattern in lower_exercise for pattern in avoid_patterns):
            flagged.append(exercise)
            replacement = None
            for pattern, substitute in substitutions.items():
                if pattern in lower_exercise:
                    replacement = substitute
                    break
            if replacement is None:
                replacement = replacements[0] if replacements else "mobility work"
            modified_exercises.append(f"{replacement} (replace {exercise})")
        else:
            modified_exercises.append(exercise)

    return modified_exercises, list(dict.fromkeys(flagged))


def _day_block(day_name: str, focus: str, exercises: List[str], duration: str, injury_context: Dict[str, Any]) -> dict:
    safe_exercises, avoided = _apply_injury_modifications(exercises, injury_context)
    return {
        "day_name": day_name,
        "focus": focus,
        "exercises": safe_exercises,
        "duration": duration,
        "warmup": _build_warmup_routine(injury_context),
        "cooldown": _build_cooldown_routine(injury_context),
        "precautions": injury_context["precautions"],
        "avoid_exercises": avoided,
        "exercise_options": injury_context["replacements"],
    }


def generate_weekly_schedule(workout_type: str, intensity: str, age: int, weight: int, profile: Dict[str, Any] | None = None) -> dict:
    """
    Generate 7-day workout schedule
    """
    injury_context = _build_injury_context(profile or {})
    
    base_schedule = {
        "Monday": _day_block(
            "Monday",
            "Chest & Triceps",
            [
                "Push-ups (3 sets x 10-15 reps)",
                "Dips (3 sets x 8-12 reps)",
                "Tricep dips (3 sets x 10 reps)",
                "Running/Cardio (10-15 mins)",
            ],
            "45-60 mins",
            injury_context,
        ),
        "Tuesday": _day_block(
            "Tuesday",
            "Back & Biceps",
            [
                "Pull-ups/Assisted pull-ups (3 sets x 8-12 reps)",
                "Rows (3 sets x 10-15 reps)",
                "Bicep curls (3 sets x 12-15 reps)",
                "Running/Cardio (10-15 mins)",
            ],
            "45-60 mins",
            injury_context,
        ),
        "Wednesday": _day_block(
            "Wednesday",
            "Legs & Core",
            [
                "Squats (3 sets x 12-15 reps)",
                "Lunges (3 sets x 10 reps per leg)",
                "Planks (3 sets x 30-60 secs)",
                "Calf raises (3 sets x 15 reps)",
                "Running/Cardio (15-20 mins)",
            ],
            "50-65 mins",
            injury_context,
        ),
        "Thursday": _day_block(
            "Thursday",
            "Active Recovery",
            [
                "Light stretching (10 mins)",
                "Yoga/Pilates (20-30 mins)",
                "Walking (20-30 mins)",
            ],
            "30-45 mins",
            injury_context,
        ),
        "Friday": _day_block(
            "Friday",
            "Shoulders & Abs",
            [
                "Shoulder presses (3 sets x 10-12 reps)",
                "Lateral raises (3 sets x 12-15 reps)",
                "Sit-ups/Crunches (3 sets x 15-20 reps)",
                "Leg raises (3 sets x 12-15 reps)",
                "Running/Cardio (10-15 mins)",
            ],
            "45-60 mins",
            injury_context,
        ),
        "Saturday": _day_block(
            "Saturday",
            "Full Body",
            [
                "Burpees (3 sets x 10 reps)",
                "Mountain climbers (3 sets x 20 reps)",
                "Jump squats (3 sets x 15 reps)",
                "Push-up to T-spine (3 sets x 10 reps)",
                "Running/Cardio (15-20 mins)",
            ],
            "50-65 mins",
            injury_context,
        ),
        "Sunday": _day_block(
            "Sunday",
            "Rest Day",
            [
                "Light stretching (15 mins)",
                "Meditation (10 mins)",
                "Walk/Nature time",
            ],
            "Flexible",
            injury_context,
        ),
    }
    
    return base_schedule


def generate_fitness_tips(goal: str, fitness_level: str, age: int) -> list:
    """
    Generate personalized fitness tips
    """
    
    tips = {
        "muscle_gain": [
            "💪 Lift heavy weights - 6-12 reps per set for muscle growth",
            "📈 Progressive overload - increase weight weekly by 2-5%",
            "😴 Sleep 8 hours daily - muscle recovery happens during sleep",
            "🔄 Train each muscle group 2x per week",
            "🧘 Rest 2-3 mins between heavy sets",
            "🏋️ Focus on compound movements: squats, deadlifts, bench press",
        ],
        "weight_loss": [
            "🏃 Cardio 4-5x per week (30-40 mins) - burns calories",
            "💪 Weight training 3x per week - preserves muscle during loss",
            "⚡ High-intensity interval training (HIIT) - effective calorie burn",
            "🔥 Aim for 500 calorie deficit daily (0.5kg/week loss)",
            "⏰ Workout early morning - boost metabolism all day",
            "🎯 Track workouts - consistency matters more than intensity",
        ],
        "maintenance": [
            "⚖️ Mix strength and cardio - 3 days each",
            "🎯 Maintain current fitness level with regular workouts",
            "📊 Track your progress - record weights and reps",
            "🔄 Change exercises every 4-6 weeks - prevent plateau",
            "😴 Sleep 7-8 hours daily",
            "🧘 Include flexibility/yoga - maintain mobility",
        ],
        "muscle_endurance": [
            "🔄 Higher reps (15-20) with moderate weight",
            "🏃 Mix strength with cardio - build stamina",
            "⚡ Circuit training - minimal rest between exercises",
            "🧠 Mental endurance - push through fatigue",
            "🥤 Hydration crucial - especially during long workouts",
            "💨 Focus on form over weight",
        ],
    }
    
    fitness_level_tips = {
        "amateur": ["Start with controlled form and full range", "Focus on consistency before intensity"],
        "sedentary": ["Start slow - 15-20 mins per session", "Build habit first - 3x per week"],
        "light": ["Increase intensity gradually", "Add 1 extra session per week"],
        "intermediate": ["Challenge yourself with heavier weights", "Try new workout styles"],
        "moderate": ["Challenge yourself with heavier weights", "Try new workout styles"],
        "professional": ["Advanced exercises - weighted pull-ups, handstands", "Plan weekly periodization to avoid plateaus"],
        "advanced": ["Advanced exercises - weighted pull-ups, handstands", "Reduce rest periods"],
        "active": ["Advanced exercises - weighted pull-ups, handstands", "Reduce rest periods"],
        "very_active": ["Train for specific goals", "Consider working with a coach"],
    }
    
    base_tips = tips.get(goal.lower(), [])
    level_tips = fitness_level_tips.get(fitness_level.lower(), [])
    
    return base_tips + level_tips


def generate_recovery_tips(intensity: str) -> list:
    """
    Generate recovery and injury prevention tips
    """
    
    recovery_tips = {
        "beginner": [
            "Rest days: 2-3 per week",
            "Stretching: 10 mins daily",
            "Sleep: 8 hours minimum",
            "Nutrition: Adequate protein + calories",
        ],
        "intermediate": [
            "Rest days: 1-2 per week",
            "Foam rolling: 2-3x per week",
            "Stretching: 15 mins daily",
            "Sleep: 8 hours minimum",
            "Recovery techniques: Cold shower/massage",
        ],
        "advanced": [
            "Strategic deloading: 1 week every 8 weeks",
            "Active recovery days: light swimming, yoga",
            "Foam rolling + stretching: Daily",
            "Sleep: 8-9 hours for adaptation",
            "Meditation: Reduce cortisol (stress hormone)",
        ],
        "elite": [
            "Periodized training: Cycles of 4-6 weeks",
            "Recovery modalities: Massage, ice baths, sauna",
            "Sleep optimization: 9+ hours",
            "Nutrition timing: Pre/post workout fueling",
            "Professional support: Trainer, nutritionist",
        ],
    }
    
    return recovery_tips.get(intensity, recovery_tips["intermediate"])
