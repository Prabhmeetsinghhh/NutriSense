"""
Exercise Preference Tracking & User Exercise History
For personalizing workout recommendations
"""

# MongoDB schema for user exercise preferences
# This will be stored in the 'user_exercise_preferences' collection

EXERCISE_PREFERENCE_SCHEMA = {
    "email": "user@example.com",
    "exercises": {
        "exercise_id": {
            "name": "Push-ups",
            "rating": 5,  # 1-5 stars
            "completed_count": 10,
            "last_performed": "2024-04-20T10:30:00",
            "personal_record": {
                "weight": 50,  # kg (if applicable)
                "reps": 25,
                "date": "2024-04-20"
            },
            "difficulty_rating": "easy",  # How user rates difficulty
            "notes": "Love this exercise, feeling strong!"
        }
    },
    "preferred_muscle_groups": ["chest", "back", "core"],
    "disliked_exercises": ["leg_curl", "leg_extension"],  # User prefers compound movements
    "difficulty_preference": "intermediate",  # beginner, intermediate, advanced
    "equipment_access": ["dumbbells", "barbell", "bench", "pull_up_bar"],  # What they have access to
    "injury_history": [
        {
            "area": "shoulder",
            "status": "recovered",
            "avoid_exercises": ["shoulder_press"],
            "modified_exercises": ["bench_press_light_weight"]
        }
    ],
    "updated_at": "2024-04-20T10:30:00",
    "created_at": "2024-04-15T08:00:00"
}

# Exercise performance tracking (separate collection for historical data)
EXERCISE_PERFORMANCE_SCHEMA = {
    "email": "user@example.com",
    "exercise_id": "push_ups",
    "exercise_name": "Push-ups",
    "session_date": "2024-04-20",
    "session_id": "SESSION_123",
    "sets": [
        {
            "set_number": 1,
            "reps": 20,
            "weight": None,  # null for bodyweight
            "rpe": 6,  # Rate of Perceived Exertion (1-10)
            "duration_seconds": 45
        },
        {
            "set_number": 2,
            "reps": 18,
            "weight": None,
            "rpe": 7,
            "duration_seconds": 50
        }
    ],
    "total_volume": 38,  # Total reps
    "difficulty_felt": "moderate",
    "notes": "Felt good, could do more",
    "muscle_soreness_next_day": 3,  # 1-5 scale
    "created_at": "2024-04-20T10:30:00"
}
