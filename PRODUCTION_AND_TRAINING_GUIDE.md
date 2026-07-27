# Production And Training Guide

## Goal

Make the backend durable for all users, keep model training reproducible, and prepare the project for a personalized diet chatbot.

## 1. Database Setup You Must Do Externally

### Required production settings

Set these environment variables in your deployment platform or local `.env` file:

```env
APP_ENV=production
MONGODB_URI=<your-real-mongodb-or-atlas-uri>
MONGODB_DB_NAME=diet_fitness_planner
MONGODB_USE_MOCK=false
MONGODB_ALLOW_MOCK_FALLBACK=false
CORS_ALLOWED_ORIGINS=<your-frontend-domain>
ML_MODEL_DIR=DietAndFitnessPlanner-BE/models
```

### What this changes

- The backend will use a real persistent MongoDB instance.
- It will not silently fall back to in-memory mock storage.
- User plans, feedback, exercise preferences, and performance history will survive restart.

### What to verify

- `GET /health` returns `database_mode: mongodb`.
- `GET /health` returns `persistent_storage: true`.
- `GET /health` returns `ml_runtime.ready: true`.

### Best MongoDB choice

Use MongoDB Atlas unless you already have a managed MongoDB service.

### Minimal production collections

- `users`
- `plan_history`
- `plan_feedback`
- `user_exercise_preferences`
- `exercise_performance`

### Recommended indexes

The backend already creates these automatically:

- `users.email` unique
- `plan_history.email + created_at`
- `plan_feedback.email + created_at`
- `plan_feedback.plan_id`

## 2. Data You Need For Model Training

### A. Goal achievement model

Use rows derived from:

- `plan_feedback`
- `users`

Useful features:

- average adherence
- adherence standard deviation
- adherence count
- adherence trend
- goal code

Target:

- `target_success` from future adherence behavior

### B. Meal adherence model

Use rows derived from:

- `plan_feedback`
- `users`

Useful features:

- average user rating
- feedback history count
- high-protein keyword flag
- vegetable keyword flag
- fried food flag
- spice-heavy flag
- text length

Target:

- `target_adherence`

### C. Food recognition model

Only train this when you have enough labeled images.

Suggested folder structure:

```text
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
```

Use at least a few hundred images per class if possible.

### D. Chatbot knowledge base

Build this from:

- plan templates
- diet rules
- exercise library
- nutrition facts
- feedback history
- goal-specific recommendations

## 3. Best Algorithms For This Project

### Keep these

- Goal achievement: `RandomForestClassifier`
- Meal adherence: `GradientBoostingClassifier`
- Exercise recommendation: rule-based ranking first
- Food recognition: `EfficientNetB0` or `MobileNetV2`
- Chatbot: RAG over your own data, not a custom-from-scratch LLM

### Why

- They are fast to train.
- They work well on tabular project data.
- They are easier to debug and explain.
- They are enough for a strong student project without overengineering.

## 4. Training Flow

### Step 1

Collect real user actions in MongoDB.

### Step 2

Export training data:

```powershell
python DietAndFitnessPlanner-BE/tools/export_ml_training_data.py
```

### Step 3

Train the models:

```powershell
python DietAndFitnessPlanner-BE/tools/train_goal_achievement_model.py
python DietAndFitnessPlanner-BE/tools/train_meal_adherence_model.py
```

### Step 4

Run the bootstrap pipeline:

```powershell
python DietAndFitnessPlanner-BE/tools/run_ml_bootstrap.py
```

### Step 5

Check the smoke test output and metrics files.

## 5. What To Finish Fast

If you want the fastest path to a solid final project, do this order:

1. Set up real MongoDB Atlas.
2. Push the backend to use real persistent storage.
3. Collect feedback through the app.
4. Retrain the goal and meal models using real data.
5. Add the chatbot with RAG.
6. Add food image classification only if you have enough images.

## 6. What Not To Depend On

- Do not depend on mock MongoDB for user data.
- Do not expect online learning from the current ML code.
- Do not train a chatbot from scratch unless you already have a large dataset.
- Do not replace the current tabular models with deep learning unless your data grows a lot.

## 7. Final Production Checklist

- [ ] Real MongoDB URI configured
- [ ] `APP_ENV=production`
- [ ] `MONGODB_ALLOW_MOCK_FALLBACK=false`
- [ ] `GET /health` shows `mongodb` mode
- [ ] `GET /health` shows `persistent_storage: true`
- [ ] Frontend allowed origin configured
- [ ] Goal model trained from real feedback
- [ ] Meal model trained from real feedback
- [ ] Chatbot knowledge base prepared
- [ ] Deployment smoke test passed
