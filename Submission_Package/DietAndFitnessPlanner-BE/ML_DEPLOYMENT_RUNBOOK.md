# ML Deployment Runbook (NutriSense)

## What this gives you now

- Data export from MongoDB training signals
- Goal achievement model training
- Meal adherence model training
- Runtime model loading with fallback logic
- Smoke test to validate outputs

## One-time setup

1. Activate backend venv
2. Install dependencies from requirements.txt
3. Copy `.env.example` to `.env` and set production values
4. Ensure MongoDB is running and reachable from the backend
5. Set `APP_ENV=production`, `MONGODB_ALLOW_MOCK_FALLBACK=false`, and a real `MONGODB_URI`

## End-to-end command

From DietAndFitnessPlanner-BE root:

```powershell
python tools/run_ml_bootstrap.py
```

This runs:
- tools/export_ml_training_data.py
- tools/train_goal_achievement_model.py
- tools/train_meal_adherence_model.py
- tools/train_food_classifier.py (only if data/food_images exists)
- tools/smoke_test_ml_pipeline.py

## Artifacts produced

- models/goal_achievement_model.joblib
- models/goal_achievement_model.metrics.json
- models/meal_adherence_model.joblib
- models/meal_adherence_model.metrics.json
- models/food_classifier.keras (optional)
- models/food_classifier.labels.json (optional)
- models/food_classifier.metrics.json (optional)
- data/training/goal_achievement_training.csv
- data/training/meal_adherence_training.csv

## Dataset structure for food model (Indian classes)

Create this folder structure before running food training:

data/food_images/
- biryani/
- dal_makhani/
- rajma_chawal/
- idli_sambar/
- poha/
- paneer_butter_masala/
- roti/
- dosa/
- upma/
- chole_bhature/

Each class folder should contain JPG or PNG images for that class.

## How backend uses trained models

At startup/import time, backend loads model artifacts from:
- ML_MODEL_DIR env var, or
- DietAndFitnessPlanner-BE/models (default)

If model files are missing or invalid, backend uses heuristic fallback.

Runtime health checks:
- `GET /health` returns database mode and model artifact status
- `GET /health/db` returns database connectivity and persistence mode

Model learning behavior:
- The app does not learn online from every request.
- User feedback is stored in MongoDB collections.
- Training scripts convert stored feedback into CSVs and retrain the saved artifacts.
- The API then loads those artifacts at startup.

## Pre-deployment checklist

1. Run bootstrap and confirm smoke test passes.
2. Check metrics files and validate baseline quality.
3. Start FastAPI and hit endpoints:
   - POST /ml/goal-achievement/{email}
   - POST /ml/predict-meal-adherence/{email}
   - GET /health
   - GET /health/db
4. Verify responses include reasonable probabilities.
5. Confirm `health.db_mode == mongodb` and `health.persistent_storage == true`.

## For Indian audience quality improvements (next sprint)

1. Add Indian food image dataset + class mapping.
2. Train image model with transfer learning (EfficientNet/MobileNet).
3. Add Hindi/hinglish meal text normalization before NLP feature extraction.
4. Retrain every week using new feedback logs.
