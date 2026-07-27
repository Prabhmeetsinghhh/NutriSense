# Exercise Database with Video Links
# Organized by muscle groups and difficulty levels
# All videos are YouTube/Vimeo embed-ready

EXERCISES_DATABASE = {
    # ==================== CHEST ====================
    "push_ups": {
        "id": "push_ups",
        "name": "Push-ups",
        "muscle_group": "chest",
        "difficulty": "beginner",
        "category": "bodyweight",
        "sets_reps": "3 x 10-15",
        "duration_minutes": 15,
        "description": "Classic bodyweight chest exercise",
        "video_url": "https://www.youtube.com/embed/IODxDxX7oi4",
        "video_platform": "youtube",
        "calories_per_set": 5,
        "equipment": "None",
        "form_tips": [
            "Keep your body straight from head to heels",
            "Lower until chest nearly touches ground",
            "Elbows at 45-degree angle",
            "Engage core throughout"
        ]
    },
    "bench_press": {
        "id": "bench_press",
        "name": "Barbell Bench Press",
        "muscle_group": "chest",
        "difficulty": "intermediate",
        "category": "strength",
        "sets_reps": "4 x 6-8",
        "duration_minutes": 20,
        "description": "Primary chest strength builder",
        "video_url": "https://www.youtube.com/embed/pPvPj3VQ1qY",
        "video_platform": "youtube",
        "calories_per_set": 8,
        "equipment": "Barbell, Bench",
        "form_tips": [
            "Feet flat on ground",
            "Shoulder blades retracted",
            "Bar at nipple level",
            "Control the descent"
        ]
    },
    "dumbbell_chest_press": {
        "id": "dumbbell_chest_press",
        "name": "Dumbbell Chest Press",
        "muscle_group": "chest",
        "difficulty": "intermediate",
        "category": "strength",
        "sets_reps": "3 x 8-10",
        "duration_minutes": 18,
        "description": "Single-arm or double-arm chest press",
        "video_url": "https://www.youtube.com/embed/FfQA-VvMfRo",
        "video_platform": "youtube",
        "calories_per_set": 6,
        "equipment": "Dumbbells",
        "form_tips": [
            "Full range of motion",
            "Squeeze at top",
            "Controlled descent"
        ]
    },
    "chest_fly": {
        "id": "chest_fly",
        "name": "Chest Fly (Machine or Dumbbells)",
        "muscle_group": "chest",
        "difficulty": "intermediate",
        "category": "isolation",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 15,
        "description": "Isolation for chest contraction",
        "video_url": "https://www.youtube.com/embed/Ce5Ygx00dQE",
        "video_platform": "youtube",
        "calories_per_set": 4,
        "equipment": "Dumbbells or Machine",
        "form_tips": [
            "Slight bend in elbows",
            "Chest-out posture",
            "Squeeze at middle"
        ]
    },
    
    # ==================== BACK ====================
    "pull_ups": {
        "id": "pull_ups",
        "name": "Pull-ups",
        "muscle_group": "back",
        "difficulty": "intermediate",
        "category": "bodyweight",
        "sets_reps": "3 x 5-10",
        "duration_minutes": 20,
        "description": "Upper back and lat builder",
        "video_url": "https://www.youtube.com/embed/eYgyNuSbyR4",
        "video_platform": "youtube",
        "calories_per_set": 7,
        "equipment": "Pull-up Bar",
        "form_tips": [
            "Grip shoulder-width apart",
            "Pull chest to bar",
            "Full range of motion",
            "Controlled descent"
        ]
    },
    "lat_pulldown": {
        "id": "lat_pulldown",
        "name": "Lat Pulldown",
        "muscle_group": "back",
        "difficulty": "beginner",
        "category": "strength",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 15,
        "description": "Machine-based lat builder",
        "video_url": "https://www.youtube.com/embed/KAL8lZRBQdE",
        "video_platform": "youtube",
        "calories_per_set": 5,
        "equipment": "Lat Pulldown Machine",
        "form_tips": [
            "Chest out",
            "Pull bar to chest",
            "Seated posture"
        ]
    },
    "barbell_row": {
        "id": "barbell_row",
        "name": "Barbell Row",
        "muscle_group": "back",
        "difficulty": "intermediate",
        "category": "strength",
        "sets_reps": "4 x 6-8",
        "duration_minutes": 20,
        "description": "Overall back mass builder",
        "video_url": "https://www.youtube.com/embed/I6l7-KY-PwA",
        "video_platform": "youtube",
        "calories_per_set": 8,
        "equipment": "Barbell",
        "form_tips": [
            "Back straight, hinge at hips",
            "Pull to lower chest",
            "Squeeze shoulder blades",
            "Explosive pull"
        ]
    },
    "dumbbell_row": {
        "id": "dumbbell_row",
        "name": "Dumbbell Row",
        "muscle_group": "back",
        "difficulty": "beginner",
        "category": "strength",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 15,
        "description": "Single-arm back builder",
        "video_url": "https://www.youtube.com/embed/w6qKwVAB-gU",
        "video_platform": "youtube",
        "calories_per_set": 5,
        "equipment": "Dumbbell",
        "form_tips": [
            "One knee on bench",
            "Retract shoulder blade",
            "Elbow to hip"
        ]
    },
    
    # ==================== SHOULDERS ====================
    "shoulder_press": {
        "id": "shoulder_press",
        "name": "Shoulder Press (Barbell or Dumbbell)",
        "muscle_group": "shoulders",
        "difficulty": "intermediate",
        "category": "strength",
        "sets_reps": "3 x 8-10",
        "duration_minutes": 18,
        "description": "Primary shoulder builder",
        "video_url": "https://www.youtube.com/embed/Vr0-KqQJLFI",
        "video_platform": "youtube",
        "calories_per_set": 6,
        "equipment": "Barbell/Dumbbells",
        "form_tips": [
            "Core braced",
            "Elbows forward",
            "Full lockout at top",
            "Controlled descent"
        ]
    },
    "lateral_raise": {
        "id": "lateral_raise",
        "name": "Lateral Raise",
        "muscle_group": "shoulders",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 12-15",
        "duration_minutes": 12,
        "description": "Side shoulder isolation",
        "video_url": "https://www.youtube.com/embed/3VcC0N5EEkA",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Dumbbells",
        "form_tips": [
            "Slight bend in elbows",
            "Raise to shoulder height",
            "Controlled descent"
        ]
    },
    "front_raise": {
        "id": "front_raise",
        "name": "Front Raise",
        "muscle_group": "shoulders",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 12,
        "description": "Front shoulder isolation",
        "video_url": "https://www.youtube.com/embed/BLPy0t65PvI",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Dumbbells/Barbell",
        "form_tips": [
            "Slight knee bend",
            "Raise to shoulder level",
            "Palms down"
        ]
    },
    
    # ==================== ARMS ====================
    "barbell_curl": {
        "id": "barbell_curl",
        "name": "Barbell Curl",
        "muscle_group": "biceps",
        "difficulty": "beginner",
        "category": "strength",
        "sets_reps": "3 x 8-10",
        "duration_minutes": 15,
        "description": "Bicep strength builder",
        "video_url": "https://www.youtube.com/embed/vF7nOUYzZAQ",
        "video_platform": "youtube",
        "calories_per_set": 4,
        "equipment": "Barbell",
        "form_tips": [
            "Elbows locked at sides",
            "Full range of motion",
            "Controlled descent"
        ]
    },
    "dumbbell_curl": {
        "id": "dumbbell_curl",
        "name": "Dumbbell Curl",
        "muscle_group": "biceps",
        "difficulty": "beginner",
        "category": "strength",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 15,
        "description": "Single-arm bicep builder",
        "video_url": "https://www.youtube.com/embed/5u-Ym1jCDhY",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Dumbbells",
        "form_tips": [
            "Palms facing forward",
            "Elbow stable",
            "Squeeze at top"
        ]
    },
    "tricep_dips": {
        "id": "tricep_dips",
        "name": "Tricep Dips",
        "muscle_group": "triceps",
        "difficulty": "intermediate",
        "category": "bodyweight",
        "sets_reps": "3 x 8-12",
        "duration_minutes": 15,
        "description": "Bodyweight tricep builder",
        "video_url": "https://www.youtube.com/embed/0326qJt6Aq0",
        "video_platform": "youtube",
        "calories_per_set": 5,
        "equipment": "Bench",
        "form_tips": [
            "Elbows at 90 degrees",
            "Full range of motion",
            "Chest-forward lean"
        ]
    },
    "tricep_pushdown": {
        "id": "tricep_pushdown",
        "name": "Tricep Pushdown",
        "muscle_group": "triceps",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 12-15",
        "duration_minutes": 12,
        "description": "Cable tricep isolation",
        "video_url": "https://www.youtube.com/embed/7lrXdEHJyAA",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Cable Machine",
        "form_tips": [
            "Elbows locked",
            "Full extension",
            "Controlled return"
        ]
    },
    
    # ==================== LEGS ====================
    "squats": {
        "id": "squats",
        "name": "Barbell Squats",
        "muscle_group": "legs",
        "difficulty": "intermediate",
        "category": "strength",
        "sets_reps": "4 x 6-8",
        "duration_minutes": 25,
        "description": "Lower body powerhouse",
        "video_url": "https://www.youtube.com/embed/iLDFubK4d6s",
        "video_platform": "youtube",
        "calories_per_set": 12,
        "equipment": "Barbell, Rack",
        "form_tips": [
            "Chest up, core braced",
            "Knees over toes",
            "Depth to parallel or below",
            "Explosive up"
        ]
    },
    "leg_press": {
        "id": "leg_press",
        "name": "Leg Press",
        "muscle_group": "legs",
        "difficulty": "beginner",
        "category": "strength",
        "sets_reps": "3 x 10-12",
        "duration_minutes": 20,
        "description": "Machine-based leg builder",
        "video_url": "https://www.youtube.com/embed/6T2gN5pJMDc",
        "video_platform": "youtube",
        "calories_per_set": 8,
        "equipment": "Leg Press Machine",
        "form_tips": [
            "Feet shoulder-width",
            "Full range of motion",
            "Don't lock knees"
        ]
    },
    "leg_extension": {
        "id": "leg_extension",
        "name": "Leg Extension",
        "muscle_group": "quads",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 12-15",
        "duration_minutes": 15,
        "description": "Quadriceps isolation",
        "video_url": "https://www.youtube.com/embed/RLM-r-vDxXo",
        "video_platform": "youtube",
        "calories_per_set": 4,
        "equipment": "Leg Extension Machine",
        "form_tips": [
            "Full extension at top",
            "Controlled descent",
            "Seat back"
        ]
    },
    "leg_curl": {
        "id": "leg_curl",
        "name": "Leg Curl",
        "muscle_group": "hamstrings",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 12-15",
        "duration_minutes": 15,
        "description": "Hamstring isolation",
        "video_url": "https://www.youtube.com/embed/1Xj7j-yJ0DI",
        "video_platform": "youtube",
        "calories_per_set": 4,
        "equipment": "Leg Curl Machine",
        "form_tips": [
            "Full curl at top",
            "Hips steady",
            "Controlled release"
        ]
    },
    "deadlifts": {
        "id": "deadlifts",
        "name": "Deadlifts",
        "muscle_group": "legs",
        "difficulty": "advanced",
        "category": "strength",
        "sets_reps": "3 x 5-6",
        "duration_minutes": 25,
        "description": "Total body strength exercise",
        "video_url": "https://www.youtube.com/embed/Op9kVJ2qvzQ",
        "video_platform": "youtube",
        "calories_per_set": 15,
        "equipment": "Barbell",
        "form_tips": [
            "Back straight, hinge at hips",
            "Shins vertical at start",
            "Explosive pull",
            "Lockout completely"
        ]
    },
    "leg_raises": {
        "id": "leg_raises",
        "name": "Lying Leg Raises",
        "muscle_group": "abs",
        "difficulty": "intermediate",
        "category": "bodyweight",
        "sets_reps": "3 x 10-15",
        "duration_minutes": 12,
        "description": "Lower ab isolation",
        "video_url": "https://www.youtube.com/embed/T4bxlMkXJuE",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Mat",
        "form_tips": [
            "Lower back pressed to floor",
            "Legs straight or bent",
            "Slow and controlled"
        ]
    },
    
    # ==================== CORE ====================
    "planks": {
        "id": "planks",
        "name": "Planks",
        "muscle_group": "core",
        "difficulty": "beginner",
        "category": "bodyweight",
        "sets_reps": "3 x 30-60 secs",
        "duration_minutes": 15,
        "description": "Core stability builder",
        "video_url": "https://www.youtube.com/embed/pSHjTRCQxIw",
        "video_platform": "youtube",
        "calories_per_set": 4,
        "equipment": "Mat",
        "form_tips": [
            "Body straight from head to heels",
            "Core braced",
            "Don't sag hips",
            "Keep breathing"
        ]
    },
    "crunches": {
        "id": "crunches",
        "name": "Crunches",
        "muscle_group": "core",
        "difficulty": "beginner",
        "category": "isolation",
        "sets_reps": "3 x 15-20",
        "duration_minutes": 12,
        "description": "Abs isolation",
        "video_url": "https://www.youtube.com/embed/MKLvKD2YoI8",
        "video_platform": "youtube",
        "calories_per_set": 2,
        "equipment": "Mat",
        "form_tips": [
            "Hands behind head",
            "Contract abs at top",
            "Slow descent"
        ]
    },
    "russian_twists": {
        "id": "russian_twists",
        "name": "Russian Twists",
        "muscle_group": "core",
        "difficulty": "intermediate",
        "category": "bodyweight",
        "sets_reps": "3 x 20 reps",
        "duration_minutes": 12,
        "description": "Oblique rotation",
        "video_url": "https://www.youtube.com/embed/OUJvNl-O_sY",
        "video_platform": "youtube",
        "calories_per_set": 3,
        "equipment": "Mat (optional weight)",
        "form_tips": [
            "Slight recline",
            "Rotate from core",
            "Explosive movement"
        ]
    },
    
    # ==================== CARDIO ====================
    "jumping_jacks": {
        "id": "jumping_jacks",
        "name": "Jumping Jacks",
        "muscle_group": "full_body",
        "difficulty": "beginner",
        "category": "cardio",
        "sets_reps": "3 x 30 secs",
        "duration_minutes": 10,
        "description": "Quick cardio warm-up",
        "video_url": "https://www.youtube.com/embed/c4bLUc6UGlY",
        "video_platform": "youtube",
        "calories_per_set": 5,
        "equipment": "None",
        "form_tips": [
            "Feet together at start",
            "Jump, spread legs and arms",
            "Continuous motion"
        ]
    },
    "burpees": {
        "id": "burpees",
        "name": "Burpees",
        "muscle_group": "full_body",
        "difficulty": "advanced",
        "category": "cardio",
        "sets_reps": "3 x 10-15",
        "duration_minutes": 15,
        "description": "Full body cardio blast",
        "video_url": "https://www.youtube.com/embed/JZQA0THl5Zw",
        "video_platform": "youtube",
        "calories_per_set": 10,
        "equipment": "None",
        "form_tips": [
            "Squat down, hands to floor",
            "Jump or step back to plank",
            "Do push-up",
            "Jump forward and up"
        ]
    },
    "mountain_climbers": {
        "id": "mountain_climbers",
        "name": "Mountain Climbers",
        "muscle_group": "full_body",
        "difficulty": "intermediate",
        "category": "cardio",
        "sets_reps": "3 x 40 secs",
        "duration_minutes": 15,
        "description": "Cardio + core",
        "video_url": "https://www.youtube.com/embed/nmwgirgXLYM",
        "video_platform": "youtube",
        "calories_per_set": 8,
        "equipment": "None",
        "form_tips": [
            "Plank position",
            "Alternate knees to chest",
            "Fast pace"
        ]
    },
}

# Muscle groups for quick lookup
MUSCLE_GROUPS = {
    "chest": ["push_ups", "bench_press", "dumbbell_chest_press", "chest_fly"],
    "back": ["pull_ups", "lat_pulldown", "barbell_row", "dumbbell_row"],
    "shoulders": ["shoulder_press", "lateral_raise", "front_raise"],
    "biceps": ["barbell_curl", "dumbbell_curl"],
    "triceps": ["tricep_dips", "tricep_pushdown"],
    "legs": ["squats", "leg_press", "leg_extension", "leg_curl", "deadlifts"],
    "quads": ["leg_extension"],
    "hamstrings": ["leg_curl"],
    "abs": ["leg_raises"],
    "core": ["planks", "crunches", "russian_twists"],
    "full_body": ["jumping_jacks", "burpees", "mountain_climbers"],
}

# Difficulty levels
DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]

# Exercise categories
EXERCISE_CATEGORIES = ["strength", "cardio", "isolation", "bodyweight"]
