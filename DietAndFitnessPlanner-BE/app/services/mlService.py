"""
Machine Learning Services for NutriSense
Handles: Food Recognition, Nutrition Prediction, Personalization, Goal Achievement, 
Meal Optimization, Fitness Performance Tracking
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta
import json
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import joblib
from PIL import Image

from app.models.exercises import EXERCISES_DATABASE, MUSCLE_GROUPS


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR = os.getenv("ML_MODEL_DIR", os.path.join(BASE_DIR, "models"))


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _goal_to_code(goal: str) -> int:
    mapping = {
        "weight_loss": 0,
        "muscle_gain": 1,
        "maintenance": 2,
        "muscle_endurance": 3,
    }
    return mapping.get(str(goal or "maintenance").lower(), 2)


def _load_model_bundle(model_name: str) -> Optional[Dict[str, Any]]:
    artifact_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")
    if not os.path.exists(artifact_path):
        return None
    try:
        bundle = joblib.load(artifact_path)
        if isinstance(bundle, dict) and "model" in bundle and "feature_order" in bundle:
            return bundle
        return None
    except Exception:
        return None


_goal_model_bundle = _load_model_bundle("goal_achievement_model")
_meal_model_bundle = _load_model_bundle("meal_adherence_model")


WORKOUT_GOAL_GROUPS = {
    "weight_loss": ["chest", "back", "legs", "shoulders", "abs", "biceps", "triceps"],
    "muscle_gain": ["chest", "back", "legs", "shoulders", "biceps", "triceps"],
    "maintenance": ["chest", "back", "legs", "shoulders", "abs", "biceps", "triceps"],
    "muscle_endurance": ["chest", "back", "legs", "shoulders", "abs", "biceps", "triceps"],
}

INJURY_RULES = {
    "disc bulge": {
        "avoid": ["deadlift", "barbell_row", "dumbbell_row", "good morning", "romanian deadlift", "rows"],
        "prefer": ["chest supported row", "lat pulldown", "glute bridge", "bird dog", "dead bug", "planks"],
        "precautions": [
            "Keep a neutral spine and avoid loaded spinal flexion.",
            "Use supported pulling movements instead of bent-over rows.",
            "Stop any exercise that triggers pain, numbness, or radiating symptoms.",
        ],
    },
    "shoulder": {
        "avoid": ["shoulder_press", "overhead press", "lateral_raise", "upright row"],
        "prefer": ["incline push-up", "chest_fly", "face pull", "planks"],
        "precautions": [
            "Avoid painful overhead ranges until symptoms settle.",
            "Use neutral grip presses and controlled tempo.",
        ],
    },
    "knee": {
        "avoid": ["burpees", "jumping_jacks", "squats", "deadlifts"],
        "prefer": ["leg_press", "step-up", "glute bridge", "planks"],
        "precautions": [
            "Use a pain-free squat depth and controlled knee tracking.",
            "Prefer lower-impact cardio and machine-based leg work.",
        ],
    },
}


def _normalize_text_list(raw_value: Any) -> List[str]:
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        return [str(item).strip().lower() for item in raw_value if str(item).strip()]
    if isinstance(raw_value, str):
        return [part.strip().lower() for part in raw_value.replace("/", ",").split(",") if part.strip()]
    return [str(raw_value).strip().lower()]


def _exercise_lookup(exercise_id: str) -> Dict[str, Any]:
    return EXERCISES_DATABASE.get(exercise_id, {})


def _format_exercise(exercise_id: str, phase: str, score: float, reason: str) -> Dict[str, Any]:
    exercise = _exercise_lookup(exercise_id)
    if not exercise:
        return {}
    return {
        "id": exercise_id,
        "name": exercise.get("name", exercise_id.replace("_", " ")),
        "muscle_group": exercise.get("muscle_group", "general"),
        "difficulty": exercise.get("difficulty", "beginner"),
        "equipment": exercise.get("equipment", "Unknown"),
        "video_url": exercise.get("video_url", ""),
        "sets_reps": exercise.get("sets_reps", ""),
        "form_tips": exercise.get("form_tips", [])[:3],
        "calories_per_set": exercise.get("calories_per_set", 0),
        "description": exercise.get("description", ""),
        "phase": phase,
        "score": round(score, 2),
        "why": reason,
    }


class FoodRecognitionService:
    """
    Image-based food identification and calorie estimation
    Uses pre-trained models for food classification
    """
    
    def __init__(self):
        self.model_loaded = False
        self.food_database = self._load_food_database()
        self.image_model = None
        self.image_labels: List[str] = []
        self._load_food_image_model()

    def _load_food_image_model(self) -> None:
        model_path = os.path.join(MODEL_DIR, "food_classifier.keras")
        labels_path = os.path.join(MODEL_DIR, "food_classifier.labels.json")

        if not os.path.exists(model_path) or not os.path.exists(labels_path):
            return

        try:
            import tensorflow as tf

            self.image_model = tf.keras.models.load_model(model_path)
            with open(labels_path, "r", encoding="utf-8") as f:
                labels = json.load(f)
            if isinstance(labels, list):
                self.image_labels = [str(x) for x in labels]
                self.model_loaded = True
        except Exception:
            self.image_model = None
            self.image_labels = []
            self.model_loaded = False

    def _predict_from_image_model(self, image_path: str) -> Optional[Dict[str, Any]]:
        if not self.model_loaded or self.image_model is None or not self.image_labels:
            return None
        if not os.path.exists(image_path):
            return None

        try:
            img = Image.open(image_path).convert("RGB").resize((224, 224))
            arr = np.asarray(img).astype(np.float32)
            arr = np.expand_dims(arr, axis=0)

            preds = self.image_model.predict(arr, verbose=0)[0]
            best_idx = int(np.argmax(preds))
            confidence = float(preds[best_idx])
            label = self.image_labels[best_idx]

            normalized_label = label.lower().replace(" ", "_")
            macro_base = self.food_database.get(
                normalized_label,
                {"calories": 240, "protein": 10, "carbs": 25, "fat": 9},
            )

            return {
                "status": "success",
                "food_item": label,
                "confidence": round(confidence, 3),
                "components": [label],
                "estimated_calories": int(macro_base["calories"] * 2),
                "macros": {
                    "protein": round(float(macro_base["protein"] * 2), 1),
                    "carbs": round(float(macro_base["carbs"] * 2), 1),
                    "fat": round(float(macro_base["fat"] * 2), 1),
                },
                "serving_size": "Approx 200g",
                "note": "Predicted using trained food image model",
                "model": "food_classifier.keras",
            }
        except Exception:
            return None
    
    def _load_food_database(self) -> Dict[str, Dict[str, Any]]:
        """Load a comprehensive food database with calories and macros"""
        return {
            "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "portion": "100g cooked"},
            "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "portion": "100g"},
            "dal": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.3, "portion": "100g cooked"},
            "paneer": {"calories": 265, "protein": 25, "carbs": 5.5, "fat": 16, "portion": "100g"},
            "vegetables": {"calories": 30, "protein": 2, "carbs": 6, "fat": 0.3, "portion": "100g"},
            "roti": {"calories": 120, "protein": 4, "carbs": 22, "fat": 1, "portion": "1 piece (30g)"},
            "eggs": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "portion": "1 large"},
            "milk": {"calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3, "portion": "100ml"},
            "almonds": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50, "portion": "100g"},
            "yogurt": {"calories": 59, "protein": 3.5, "carbs": 4.7, "fat": 0.4, "portion": "100g"},
        }
    
    def recognize_food_from_image(self, image_path: str) -> Dict[str, Any]:
        """
        Simulate food recognition from image path
        In production, this would use a pre-trained CNN model
        """
        model_result = self._predict_from_image_model(image_path)
        if model_result:
            return model_result

        return {
            "status": "success",
            "food_item": "Rice with Dal",
            "confidence": 0.92,
            "components": ["rice", "dal", "vegetables"],
            "estimated_calories": 350,
            "macros": {
                "protein": 12,
                "carbs": 55,
                "fat": 5
            },
            "serving_size": "1 plate (300g)",
            "note": "Image recognition in beta. Please verify and adjust if needed."
        }
    
    def predict_nutrition_from_text(self, food_description: str) -> Dict[str, Any]:
        """
        Predict nutrition facts from text description
        E.g., "2 cups rice with chicken and vegetables"
        """
        text_lower = food_description.lower()
        
        # Simple pattern matching for now (will be replaced with ML model)
        estimated_macros = {
            "protein": 20,
            "carbs": 50,
            "fat": 15,
            "calories": 450
        }
        
        # Adjust based on keywords
        if "chicken" in text_lower or "meat" in text_lower:
            estimated_macros["protein"] += 15
            estimated_macros["calories"] += 100
        
        if "rice" in text_lower or "bread" in text_lower:
            estimated_macros["carbs"] += 20
            estimated_macros["calories"] += 150
        
        if "oil" in text_lower or "butter" in text_lower:
            estimated_macros["fat"] += 10
            estimated_macros["calories"] += 90
        
        return {
            "status": "success",
            "food_description": food_description,
            "confidence": 0.75,
            "estimated_macros": estimated_macros,
            "note": "This is an estimate based on text. Actual values may vary significantly."
        }


class ExercisePersonalizationService:
    """
    Predict nutrition needs and meal recommendations based on user profile
    """

    @staticmethod
    def _build_context(user_preferences: Dict[str, Any], performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        injuries = user_preferences.get("injury_history", [])
        injury_notes = _normalize_text_list(user_preferences.get("injury_notes"))
        avoid_exercises = set(_normalize_text_list(user_preferences.get("avoid_exercises")))
        disliked_exercises = set(_normalize_text_list(user_preferences.get("disliked_exercises")))
        preferred_muscles = _normalize_text_list(user_preferences.get("preferred_muscle_groups"))
        equipment_access = set(_normalize_text_list(user_preferences.get("equipment_access")))
        goal = str(user_preferences.get("goal", "maintenance")).lower()
        difficulty = str(user_preferences.get("difficulty_preference", user_preferences.get("fitness_level", "moderate"))).lower()
        prefer_compound = bool(user_preferences.get("prefer_compound", False))

        injury_context: List[Dict[str, Any]] = []
        for entry in injuries if isinstance(injuries, list) else []:
            if not isinstance(entry, dict):
                continue
            area = str(entry.get("area", "")).strip().lower()
            if not area:
                continue
            rules = INJURY_RULES.get(area, {})
            injury_context.append(
                {
                    "area": area,
                    "status": str(entry.get("status", "active")).lower(),
                    "avoid_exercises": _normalize_text_list(entry.get("avoid_exercises")),
                    "modified_exercises": _normalize_text_list(entry.get("modified_exercises")),
                    "precautions": rules.get("precautions", []),
                }
            )
            avoid_exercises.update(_normalize_text_list(entry.get("avoid_exercises")))
            for item in _normalize_text_list(entry.get("modified_exercises")):
                avoid_exercises.add(item)
            for item in rules.get("avoid", []):
                avoid_exercises.add(item)

        for note in injury_notes:
            rules = INJURY_RULES.get(note, {})
            for item in rules.get("avoid", []):
                avoid_exercises.add(item)
            # Promote free-text injury notes into structured injury context
            # so warmup/cooldown/safety guidance is generated consistently.
            if rules and not any(entry.get("area") == note for entry in injury_context):
                injury_context.append(
                    {
                        "area": note,
                        "status": "active",
                        "avoid_exercises": rules.get("avoid", []),
                        "modified_exercises": rules.get("prefer", []),
                        "precautions": rules.get("precautions", []),
                    }
                )

        recent_exercises = [str(item.get("exercise_id", "")).lower() for item in performance_history if isinstance(item, dict)]

        return {
            "goal": goal,
            "difficulty": difficulty,
            "prefer_compound": prefer_compound,
            "preferred_muscles": preferred_muscles,
            "equipment_access": equipment_access,
            "avoid_exercises": avoid_exercises,
            "injury_context": injury_context,
            "injury_notes": injury_notes,
            "recent_exercises": recent_exercises,
        }

    @staticmethod
    def _exercise_score(exercise_id: str, exercise: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []
        exercise_name = str(exercise.get("name", exercise_id)).lower()
        muscle_group = str(exercise.get("muscle_group", "general")).lower()
        equipment = str(exercise.get("equipment", "")).lower()
        difficulty = str(exercise.get("difficulty", "beginner")).lower()

        if exercise_id in context["avoid_exercises"] or exercise_name in context["avoid_exercises"]:
            return -100.0, ["Excluded by injury or avoid list"]

        category = str(exercise.get("category", "")).lower()
        if context["prefer_compound"] and category in {"strength", "bodyweight"}:
            score += 2.0
            reasons.append("Matches compound preference")

        if muscle_group in context["preferred_muscles"]:
            score += 2.0
            reasons.append("Targets a preferred muscle group")

        goal_groups = WORKOUT_GOAL_GROUPS.get(context["goal"], WORKOUT_GOAL_GROUPS["maintenance"])
        if muscle_group in goal_groups:
            score += 1.5
            reasons.append("Matches training goal")

        if not context["equipment_access"]:
            score += 0.5
        elif any(item in equipment for item in context["equipment_access"]):
            score += 1.5
            reasons.append("Fits available equipment")
        elif equipment == "bodyweight":
            score += 1.0
            reasons.append("Accessible without equipment")
        else:
            score -= 1.0
            reasons.append("May need unavailable equipment")

        difficulty_rank = {"beginner": 0, "easy": 0, "intermediate": 1, "moderate": 1, "advanced": 2, "hard": 2}
        user_rank = difficulty_rank.get(context["difficulty"], 1)
        exercise_rank = difficulty_rank.get(difficulty, 1)
        if exercise_rank <= user_rank:
            score += 1.0
        else:
            score -= 0.5
            reasons.append("May be too demanding right now")

        if exercise_id in context["recent_exercises"]:
            score -= 0.6
            reasons.append("Rotated to avoid repetition")

        if any(keyword in exercise_name for keyword in ["supported", "machine", "bridge", "plank", "dead bug", "carry"]):
            score += 0.8
            reasons.append("Stability-friendly choice")

        return score, reasons

    @staticmethod
    def _build_phase(exercises: List[Dict[str, Any]], phase: str) -> List[Dict[str, Any]]:
        return [
            {
                **item,
                "phase": phase,
            }
            for item in exercises
        ]

    @staticmethod
    def _build_warmup(context: Dict[str, Any]) -> List[str]:
        warmup = ["5 minutes of light cardio or brisk walking", "Dynamic joint circles and mobility work"]
        if context["injury_context"]:
            warmup.append("Pain-free activation drills for the affected area")
        if "legs" in context["preferred_muscles"]:
            warmup.append("Glute bridges, hip hinges, and bodyweight squats to tolerance")
        return warmup[:4]

    @staticmethod
    def _build_cooldown(context: Dict[str, Any]) -> List[str]:
        cooldown = ["3-5 minutes of easy walking", "Slow nasal breathing to bring heart rate down"]
        if context["injury_context"]:
            cooldown.append("Gentle mobility for the affected joints without forcing range")
        cooldown.append("Light stretching for the muscle groups trained today")
        return cooldown[:4]

    @staticmethod
    def personalize_exercise_plan(email: str, user_preferences: Dict[str, Any],
                                  performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a structured, personalized workout blueprint.
        """

        context = ExercisePersonalizationService._build_context(user_preferences, performance_history)
        goal_groups = WORKOUT_GOAL_GROUPS.get(context["goal"], WORKOUT_GOAL_GROUPS["maintenance"])

        scored_exercises: List[Tuple[float, str, Dict[str, Any], List[str]]] = []
        for exercise_id, exercise in EXERCISES_DATABASE.items():
            score, reasons = ExercisePersonalizationService._exercise_score(exercise_id, exercise, context)
            if score <= -50:
                continue
            scored_exercises.append((score, exercise_id, exercise, reasons))

        scored_exercises.sort(key=lambda item: (item[0], item[2].get("muscle_group", "")), reverse=True)

        selected: List[Dict[str, Any]] = []
        selected_muscles: set[str] = set()
        substitutions: List[Dict[str, str]] = []
        fallback_candidates: List[Dict[str, Any]] = []

        for score, exercise_id, exercise, reasons in scored_exercises:
            muscle_group = str(exercise.get("muscle_group", "general")).lower()
            formatted = _format_exercise(
                exercise_id,
                "main",
                score,
                "; ".join(reasons) if reasons else "Balanced training choice",
            )
            if not formatted:
                continue

            if muscle_group in goal_groups and muscle_group not in selected_muscles:
                selected.append(formatted)
                selected_muscles.add(muscle_group)
            elif len(selected) < 6:
                fallback_candidates.append(formatted)

            if len(selected) >= 6:
                break

        for item in fallback_candidates:
            if len(selected) >= 6:
                break
            selected.append(item)

        if not selected:
            selected = [
                {
                    "id": "bodyweight_squat",
                    "name": "Bodyweight Squat",
                    "muscle_group": "legs",
                    "difficulty": "beginner",
                    "equipment": "bodyweight",
                    "video_url": "",
                    "sets_reps": "2-3 sets x 10-15 reps",
                    "form_tips": ["Move within a pain-free range", "Keep the chest tall"],
                    "calories_per_set": 20,
                    "description": "Safe fallback movement",
                    "phase": "main",
                    "score": 0.0,
                    "why": "Fallback choice",
                }
            ]

        injured_areas = [item["area"] for item in context["injury_context"]]
        safety_notes = []
        for injury in context["injury_context"]:
            safety_notes.extend(injury.get("precautions", []))
        if not safety_notes:
            safety_notes = [
                "Start with lighter loads and progress gradually.",
                "Stop any movement that causes sharp pain or joint irritation.",
            ]

        if selected:
            for item in selected[:3]:
                substitutions.append(
                    {
                        "exercise": item["name"],
                        "safer_alternative": item["name"],
                    }
                )

        workout_focus = ", ".join(goal_groups[:3]).replace("_", " ")
        weekly_structure = {
            "sessions_per_week": 3 if context["difficulty"] in {"beginner", "easy"} else 4,
            "focus": workout_focus,
            "split": [
                "Day 1: strength focus",
                "Day 2: mobility + conditioning",
                "Day 3: upper/lower balance",
                "Day 4: recovery or accessory work" if context["difficulty"] not in {"beginner", "easy"} else "",
            ],
        }

        return {
            "status": "success",
            "email": email,
            "training_goal": context["goal"],
            "injury_context": injured_areas,
            "warmup": ExercisePersonalizationService._build_warmup(context),
            "cooldown": ExercisePersonalizationService._build_cooldown(context),
            "safety_notes": safety_notes[:4],
            "exercise_swaps": substitutions[:4],
            "weekly_structure": weekly_structure,
            "recommended_exercises": ExercisePersonalizationService._build_phase(selected, "main"),
            "exercise_ids": [item["id"] for item in selected],
            "confidence": round(min(0.55 + len(selected) * 0.05, 0.95), 2),
            "note": "Generated from goals, equipment access, injury context, and recent performance history.",
        }
    
    @staticmethod
    def predict_daily_macros(user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Heuristic daily macronutrient recommendation.
        Expects `user_profile` to contain: weight (kg), age, fitness_level, goal.
        Returns calories and macronutrient split in grams and percentages.
        """
        weight = float(user_profile.get("weight", 70))
        goal = str(user_profile.get("goal", "maintenance")).lower()

        # Base calories: simple heuristic 25 kcal/kg
        kcal_per_kg = 25
        calories = kcal_per_kg * weight
        if goal == "weight_loss":
            calories = max(1200, calories - 500)
        elif goal == "muscle_gain":
            calories = calories + 300

        # Default macro percentages
        protein_percentage = 0.30
        carbs_percentage = 0.45
        fat_percentage = 0.25

        protein_grams = round((calories * protein_percentage) / 4.0, 1)
        carbs_grams = round((calories * carbs_percentage) / 4.0, 1)
        fat_grams = round((calories * fat_percentage) / 9.0, 1)

        return {
            "calories": int(round(calories)),
            "protein_grams": protein_grams,
            "carbs_grams": carbs_grams,
            "fat_grams": fat_grams,
            "protein_percentage": int(protein_percentage * 100),
            "carbs_percentage": int(carbs_percentage * 100),
            "fat_percentage": int(fat_percentage * 100),
            "note": "Heuristic estimate — use real nutrition model for production",
        }

    @staticmethod
    def predict_meal_timing(user_profile: Dict[str, Any], workout_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Predict optimal meal timing based on activity patterns
        """
        return {
            "pre_workout": "60-90 mins before - carbs + light protein",
            "post_workout": "Within 30 mins - protein + carbs for recovery",
            "breakfast": "Upon waking - protein to break overnight fast",
            "lunch": "12-1 PM - largest meal with balanced macros",
            "dinner": "7-8 PM - moderate calories, avoid excess before sleep",
            "snacks": "Between meals to maintain steady energy and protein intake",
        }


class ExercisePersonalizationLegacyService:
    """
    Personalize exercise recommendations based on user history and preferences
    """
    
    @staticmethod
    def cluster_similar_users(user_data: List[Dict[str, Any]], n_clusters: int = 5) -> Dict[str, Any]:
        """
        Cluster users to find similar profiles
        Useful for collaborative filtering recommendations
        """
        # In production, use actual user data from database
        return {
            "status": "success",
            "clusters_found": n_clusters,
            "note": "Clustering requires historical user data"
        }
    
    @staticmethod
    def personalize_exercise_plan(email: str, user_preferences: Dict[str, Any], 
                                  performance_history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Generate personalized exercise recommendations based on:
        - User preferences (liked/disliked exercises)
        - Performance history (what they're good at)
        - Goals (muscle gain, weight loss, etc.)
        """
        
        recommendations = []
        
        # If user prefers compound movements, recommend more of those
        if user_preferences.get("prefer_compound", False):
            recommendations.extend([
                "squats", "deadlifts", "barbell_row", "bench_press"
            ])
        else:
            # Mix of compound and isolation
            recommendations.extend([
                "leg_press", "dumbbell_row", "chest_fly", "lateral_raise"
            ])
        
        # Add cardio based on goal
        goal = user_preferences.get("goal", "maintenance")
        if goal == "weight_loss":
            recommendations.extend(["mountain_climbers", "burpees"])
        elif goal == "muscle_gain":
            recommendations.extend(["pull_ups", "dips"])
        else:
            recommendations.extend(["jumping_jacks"])
        
        return recommendations
    
    @staticmethod
    def predict_workout_difficulty(email: str, exercises: List[str]) -> Dict[str, Any]:
        """
        Predict how difficult a proposed workout will be for the user
        Based on their history
        """
        return {
            "estimated_difficulty": "moderate",
            "estimated_duration_minutes": 50,
            "expected_rpe": 6,  # Rate of Perceived Exertion 1-10
            "confidence": 0.65,
            "note": "Requires historical performance data for accuracy"
        }


class NutritionPredictionService:
    """
    Nutrition-related recommendation entry points.
    """

    @staticmethod
    def predict_daily_macros(user_profile: Dict[str, Any]) -> Dict[str, Any]:
        return ExercisePersonalizationService.predict_daily_macros(user_profile)

    @staticmethod
    def predict_meal_timing(user_profile: Dict[str, Any], workout_time: Optional[str] = None) -> Dict[str, Any]:
        return ExercisePersonalizationService.predict_meal_timing(user_profile, workout_time)


class GoalAchievementPredictorService:
    """
    Predict likelihood of achieving fitness/nutrition goals
    """
    
    @staticmethod
    def predict_goal_achievement(email: str, goal: str, adherence_history: List[float]) -> Dict[str, Any]:
        """
        Predict if user will achieve their goal based on:
        - Goal type (weight loss target, muscle gain target)
        - Historical adherence %
        - Timeframe
        """
        
        if not adherence_history:
            return {"success_probability": 0.5, "confidence": 0.3, "note": "Need more data"}
        
        avg_adherence = np.mean(adherence_history)
        adherence_std = np.std(adherence_history) if len(adherence_history) > 1 else 0.0
        adherence_trend = 0.0
        if len(adherence_history) > 1:
            adherence_trend = adherence_history[-1] - adherence_history[0]

        if _goal_model_bundle:
            feature_map = {
                "avg_adherence": _safe_float(avg_adherence),
                "adherence_std": _safe_float(adherence_std),
                "adherence_count": float(len(adherence_history)),
                "adherence_trend": _safe_float(adherence_trend),
                "goal_code": float(_goal_to_code(goal)),
            }
            feature_order = _goal_model_bundle["feature_order"]
            model = _goal_model_bundle["model"]
            x = pd.DataFrame([{col: feature_map.get(col, 0.0) for col in feature_order}], columns=feature_order)
            try:
                if hasattr(model, "predict_proba"):
                    probability = float(model.predict_proba(x)[0][1])
                else:
                    pred = float(model.predict(x)[0])
                    probability = max(0.0, min(1.0, pred))
            except Exception:
                probability = min(avg_adherence / 100, 1.0)
        else:
            probability = min(avg_adherence / 100, 1.0)
        
        if probability > 0.7:
            recommendation = "Maintain consistency and progressive overload"
        elif probability > 0.5:
            recommendation = "Improve adherence and weekly recovery quality"
        else:
            recommendation = "Prioritize consistency, sleep, and simpler routines"
        
        return {
            "goal": goal,
            "success_probability": round(probability, 2),
            "average_adherence": round(float(avg_adherence), 1),
            "recommendation": recommendation,
            "confidence": min(len(adherence_history) / 20, 1.0),
            "model": "trained_model" if _goal_model_bundle else "heuristic_baseline",
        }
    
    @staticmethod
    def predict_timeline_to_goal(current_weight: float, goal_weight: float, 
                                weekly_adherence: float) -> Dict[str, Any]:
        """
        Estimate weeks needed to reach weight goal
        Based on typical 0.5-1 kg per week loss rate
        """
        weight_diff = abs(current_weight - goal_weight)
        
        if weekly_adherence < 0.5:
            rate = 0.25  # kg per week at low adherence
        elif weekly_adherence < 0.8:
            rate = 0.5
        else:
            rate = 0.75
        
        weeks_needed = weight_diff / rate
        
        return {
            "current_weight": current_weight,
            "goal_weight": goal_weight,
            "weekly_weight_change_kg": rate,
            "estimated_weeks": round(weeks_needed),
            "estimated_date": (datetime.now() + timedelta(weeks=weeks_needed)).date().isoformat(),
        }


class MealPlanOptimizationService:
    """
    Optimize meal plans using ML based on user feedback and preferences
    """
    
    @staticmethod
    def optimize_meal_plan(email: str, current_meals: Dict[str, str], 
                          user_feedback: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Suggest meal swaps to optimize for:
        - Better adherence (tastier options)
        - Cost reduction
        - Nutritional balance
        - Diversity
        """
        
        # Aggregate user feedback to find patterns
        liked_meals = []
        disliked_meals = []
        high_cost_meals = []
        
        for feedback in user_feedback:
            if feedback.get("rating", 3) >= 4:
                liked_meals.append(feedback.get("meal"))
            elif feedback.get("rating") <= 2:
                disliked_meals.append(feedback.get("meal"))
            
            if feedback.get("cost_feedback") == "expensive":
                high_cost_meals.append(feedback.get("meal"))
        
        # Simple optimization: increase liked meals, replace disliked ones
        recommendations = {
            "increase_frequency": liked_meals[:3],
            "replace_with_cheaper": high_cost_meals[:2] if high_cost_meals else [],
            "remove_disliked": disliked_meals[:2] if disliked_meals else [],
            "optimization_focus": "balanced" if not high_cost_meals else "cost"
        }
        
        return recommendations
    
    @staticmethod
    def predict_meal_adherence(email: str, proposed_meal: str, 
                              user_history: List[Dict[str, Any]]) -> float:
        """
        Predict likelihood user will stick to a proposed meal (0-1)
        Based on their history with similar meals
        """
        text = (proposed_meal or "").lower()
        has_high_protein = int(any(k in text for k in ["chicken", "paneer", "dal", "egg", "fish", "soy"]))
        has_veg = int(any(k in text for k in ["salad", "vegetable", "sabzi", "greens"]))
        is_fried = int(any(k in text for k in ["fried", "pakora", "bhatura", "chips"]))
        spice_heavy = int(any(k in text for k in ["very spicy", "spicy", "masala"]))

        avg_user_rating = 3.0
        if user_history:
            ratings = [
                _safe_float(item.get("rating"), 0.0)
                for item in user_history
                if item.get("rating") is not None
            ]
            if ratings:
                avg_user_rating = float(np.mean(ratings))

        if _meal_model_bundle:
            feature_map = {
                "avg_user_rating": _safe_float(avg_user_rating),
                "history_count": float(len(user_history or [])),
                "has_high_protein": float(has_high_protein),
                "has_veg": float(has_veg),
                "is_fried": float(is_fried),
                "spice_heavy": float(spice_heavy),
                "text_len": float(len(text)),
            }
            feature_order = _meal_model_bundle["feature_order"]
            model = _meal_model_bundle["model"]
            x = pd.DataFrame([{col: feature_map.get(col, 0.0) for col in feature_order}], columns=feature_order)
            try:
                if hasattr(model, "predict_proba"):
                    adherence = float(model.predict_proba(x)[0][1])
                else:
                    pred = float(model.predict(x)[0])
                    adherence = max(0.0, min(1.0, pred))
                return round(adherence, 3)
            except Exception:
                pass

        # Heuristic fallback tuned for Indian meal context and sustainability
        score = 0.55
        score += 0.12 if has_high_protein else 0.0
        score += 0.08 if has_veg else 0.0
        score -= 0.1 if is_fried else 0.0
        score -= 0.04 if spice_heavy else 0.0
        score += (avg_user_rating - 3.0) * 0.06
        return round(max(0.05, min(score, 0.95)), 3)


class FitnessPerformanceTrackingService:
    """
    Track and predict fitness performance improvements
    """
    
    @staticmethod
    def predict_strength_progression(email: str, exercise_id: str, 
                                    performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict next reasonable weight/reps for an exercise
        Based on progression patterns
        """
        if not performance_history:
            return {"status": "insufficient_data", "recommendation": "Complete 3+ sessions first"}
        
        # Extract progression data
        weights = []
        dates = []
        
        for perf in performance_history:
            if "weight" in perf:
                weights.append(perf["weight"])
                dates.append(perf.get("date"))
        
        if len(weights) < 2:
            return {"status": "insufficient_data"}
        
        # Simple linear regression
        avg_increase_per_week = (weights[-1] - weights[0]) / len(weights)
        
        return {
            "current_best": weights[-1],
            "average_weekly_increase": round(avg_increase_per_week, 1),
            "predicted_next_session": round(weights[-1] + (avg_increase_per_week * 0.5), 1),
            "confidence": min(len(weights) / 10, 1.0),
        }
    
    @staticmethod
    def predict_recovery_needs(email: str, recent_workouts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict recovery needs based on workout intensity and frequency
        """
        if not recent_workouts:
            return {"recovery_hours": 48, "note": "Default recovery period"}
        
        # Calculate total volume from last 7 days
        total_volume = sum(w.get("volume", 0) for w in recent_workouts[-7:])
        
        if total_volume > 100:
            recovery_hours = 72
            intensity_level = "high"
        elif total_volume > 50:
            recovery_hours = 48
            intensity_level = "moderate"
        else:
            recovery_hours = 24
            intensity_level = "low"
        
        return {
            "recommended_recovery_hours": recovery_hours,
            "intensity_level": intensity_level,
            "suggestions": [
                "Get 7-9 hours sleep",
                "Consume adequate protein (0.8-1g per lb bodyweight)",
                "Stay hydrated",
                "Consider light activity like walking"
            ]
        }


class MLPipelineService:
    """
    Orchestrates all ML services and coordinates predictions
    """
    
    @staticmethod
    def get_personalized_recommendations(email: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive ML-based recommendations
        Combines all ML services
        """
        
        goals = {
            "nutrition": NutritionPredictionService.predict_daily_macros(user_profile),
            "meal_timing": NutritionPredictionService.predict_meal_timing(user_profile),
            "exercise_personalization": ExercisePersonalizationService.personalize_exercise_plan(
                email, user_profile, user_profile.get("performance_history", [])
            ),
            "goal_achievement": GoalAchievementPredictorService.predict_goal_achievement(
                email, user_profile.get("goal"), []
            ),
        }
        
        return {
            "status": "success",
            "email": email,
            "generated_at": datetime.now().isoformat(),
            "recommendations": goals,
            "workout_blueprint": goals["exercise_personalization"],
        }


def get_ml_runtime_status() -> Dict[str, Any]:
    """Report whether the runtime is using trained artifacts or heuristic fallback."""
    critical_missing_artifacts: List[str] = []
    optional_missing_artifacts: List[str] = []
    if _goal_model_bundle is None:
        critical_missing_artifacts.append("goal_achievement_model.joblib")
    if _meal_model_bundle is None:
        critical_missing_artifacts.append("meal_adherence_model.joblib")
    if not food_recognition_service.model_loaded:
        optional_missing_artifacts.append("food_classifier.keras")

    ready = not critical_missing_artifacts

    return {
        "model_dir": MODEL_DIR,
        "goal_model_loaded": _goal_model_bundle is not None,
        "meal_model_loaded": _meal_model_bundle is not None,
        "food_model_loaded": food_recognition_service.model_loaded,
        "online_learning": False,
        "ready": ready,
        "mode": "artifact-backed" if ready else "partial-fallback",
        "critical_missing_artifacts": critical_missing_artifacts,
        "optional_missing_artifacts": optional_missing_artifacts,
    }


# Service instances
food_recognition_service = FoodRecognitionService()
nutrition_prediction_service = NutritionPredictionService()
exercise_personalization_service = ExercisePersonalizationService()
goal_achievement_service = GoalAchievementPredictorService()
meal_optimization_service = MealPlanOptimizationService()
performance_tracking_service = FitnessPerformanceTrackingService()
ml_pipeline_service = MLPipelineService()
