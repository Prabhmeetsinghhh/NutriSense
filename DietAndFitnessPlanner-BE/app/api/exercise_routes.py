from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.api.notification_routes import create_user_notification
from app.db.mongo import get_database
from app.models.exercises import EXERCISES_DATABASE, MUSCLE_GROUPS

router = APIRouter()


@router.get("/exercises")
def get_all_exercises() -> Dict[str, Any]:
    return {
        "status": "success",
        "count": len(EXERCISES_DATABASE),
        "exercises": EXERCISES_DATABASE,
        "muscle_groups": MUSCLE_GROUPS,
    }


@router.get("/exercises/{exercise_id}")
def get_exercise_by_id(exercise_id: str) -> Dict[str, Any]:
    exercise = EXERCISES_DATABASE.get(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail=f"Exercise '{exercise_id}' not found")

    return {
        "status": "success",
        "exercise": exercise,
    }


@router.get("/exercises/muscle/{muscle_group}")
def get_exercises_by_muscle_group(muscle_group: str) -> Dict[str, Any]:
    exercises = MUSCLE_GROUPS.get(muscle_group.lower(), [])
    if not exercises:
        raise HTTPException(status_code=404, detail=f"Muscle group '{muscle_group}' not found")

    exercise_details = [EXERCISES_DATABASE.get(ex_id) for ex_id in exercises if ex_id in EXERCISES_DATABASE]

    return {
        "status": "success",
        "muscle_group": muscle_group,
        "count": len(exercise_details),
        "exercises": exercise_details,
    }


@router.post("/exercise-preferences/{email}")
def save_exercise_preference(email: str, data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_email = email.strip().lower()
    exercise_id = str(data.get("exercise_id", "")).strip()
    rating = int(data.get("rating", 3))

    if not exercise_id or exercise_id not in EXERCISES_DATABASE:
        raise HTTPException(status_code=400, detail="Invalid exercise_id")
    if not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    db = get_database()
    now = datetime.now(timezone.utc)

    preferences_collection = db["user_exercise_preferences"]
    exercise_info = EXERCISES_DATABASE[exercise_id]

    update_data = {
        f"exercises.{exercise_id}": {
            "name": exercise_info.get("name"),
            "rating": rating,
            "last_performed": now,
            "notes": str(data.get("notes", "")).strip(),
            "difficulty_rating": str(data.get("difficulty_rating", "moderate")).lower(),
        }
    }

    if "personal_record" in data and data["personal_record"]:
        update_data[f"exercises.{exercise_id}"]["personal_record"] = data["personal_record"]

    preferences_collection.update_one(
        {"email": normalized_email},
        {
            "$set": update_data,
            "$setOnInsert": {
                "email": normalized_email,
                "created_at": now,
                "exercises": {},
            }
        },
        upsert=True,
    )

    if data.get("sets"):
        performance_collection = db["exercise_performance"]
        performance_doc = {
            "email": normalized_email,
            "exercise_id": exercise_id,
            "exercise_name": exercise_info.get("name"),
            "session_date": now.date().isoformat(),
            "sets": data.get("sets"),
            "difficulty_felt": str(data.get("difficulty_felt", "moderate")).lower(),
            "notes": str(data.get("notes", "")).strip(),
            "created_at": now,
        }
        performance_collection.insert_one(performance_doc)

    create_user_notification(
        normalized_email,
        title="Exercise preference saved",
        message=f"We saved your feedback for {exercise_info.get('name')} and will use it in future workout suggestions.",
        notification_type="info",
        action_label="View workout",
        action_path="/result",
        source="exercise_feedback",
        priority="normal",
    )

    return {
        "status": "success",
        "message": f"Preference saved for {exercise_info.get('name')}",
        "email": normalized_email,
        "exercise_id": exercise_id,
    }


@router.get("/exercise-preferences/{email}")
def get_user_exercise_preferences(email: str) -> Dict[str, Any]:
    normalized_email = email.strip().lower()
    db = get_database()

    prefs_collection = db["user_exercise_preferences"]
    prefs = prefs_collection.find_one({"email": normalized_email})

    perf_collection = db["exercise_performance"]
    recent_performance = list(
        perf_collection
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(20)
    )

    return {
        "status": "success",
        "email": normalized_email,
        "preferences": prefs if prefs else {"email": normalized_email, "exercises": {}},
        "recent_performance": [
            {
                "id": str(p.get("_id")),
                "exercise_id": p.get("exercise_id"),
                "exercise_name": p.get("exercise_name"),
                "session_date": p.get("session_date"),
                "difficulty_felt": p.get("difficulty_felt"),
                "created_at": p.get("created_at"),
            }
            for p in recent_performance
        ],
    }


@router.get("/exercises/difficulty/{level}")
def get_exercises_by_difficulty(level: str) -> Dict[str, Any]:
    valid_levels = ["beginner", "intermediate", "advanced"]
    if level.lower() not in valid_levels:
        raise HTTPException(status_code=400, detail=f"Level must be one of {valid_levels}")

    exercises = {
        ex_id: ex for ex_id, ex in EXERCISES_DATABASE.items()
        if ex.get("difficulty") == level.lower()
    }

    return {
        "status": "success",
        "difficulty_level": level,
        "count": len(exercises),
        "exercises": exercises,
    }


@router.post("/exercise-feedback/{email}/{exercise_id}")
def submit_exercise_feedback(email: str, exercise_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_email = email.strip().lower()

    if exercise_id not in EXERCISES_DATABASE:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db = get_database()
    feedback_collection = db["exercise_feedback"]

    feedback_doc = {
        "email": normalized_email,
        "exercise_id": exercise_id,
        "exercise_name": EXERCISES_DATABASE[exercise_id].get("name"),
        "rpe": int(data.get("rpe", 5)),
        "difficulty_felt": str(data.get("difficulty_felt", "moderate")).lower(),
        "muscle_soreness": int(data.get("muscle_soreness", 0)),
        "would_repeat": bool(data.get("would_repeat", True)),
        "notes": str(data.get("notes", "")).strip(),
        "session_date": data.get("session_date", datetime.now(timezone.utc).isoformat()),
        "created_at": datetime.now(timezone.utc),
    }

    inserted = feedback_collection.insert_one(feedback_doc)

    create_user_notification(
        normalized_email,
        title="Workout feedback saved",
        message="Your workout feedback is stored. The next plan can adapt based on your ratings and recovery.",
        notification_type="success",
        action_label="Back to plan",
        action_path="/result",
        source="exercise_feedback",
        priority="normal",
    )

    return {
        "status": "success",
        "message": "Feedback saved",
        "feedback_id": str(inserted.inserted_id),
    }
