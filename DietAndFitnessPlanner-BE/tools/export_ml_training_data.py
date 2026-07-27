import os
import sys
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd

# Allow running as a script from DietAndFitnessPlanner-BE/tools
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.db.mongo import connect_to_mongo, close_mongo_connection  # noqa: E402


def _goal_to_code(goal: str) -> int:
    mapping = {
        "weight_loss": 0,
        "muscle_gain": 1,
        "maintenance": 2,
        "muscle_endurance": 3,
    }
    return mapping.get(str(goal or "maintenance").lower(), 2)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _contains_any(text: str, keywords: List[str]) -> int:
    text_lower = (text or "").lower()
    return int(any(k in text_lower for k in keywords))


def _extract_goal_training_rows(db) -> List[Dict[str, Any]]:
    feedback_docs = list(
        db["plan_feedback"]
        .find({}, {"email": 1, "adherence_percent": 1, "created_at": 1})
        .sort([("email", 1), ("created_at", 1)])
    )

    user_goal = {}
    for row in db["users"].find({}, {"email": 1, "goal": 1}):
        user_goal[str(row.get("email", "")).strip().lower()] = str(row.get("goal", "maintenance"))

    # Build sequential training examples: predict next adherence success from past adherence behavior.
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for doc in feedback_docs:
        email = str(doc.get("email", "")).strip().lower()
        if not email:
            continue
        grouped.setdefault(email, []).append(doc)

    rows: List[Dict[str, Any]] = []
    for email, docs in grouped.items():
        adherence_values = [_safe_float(d.get("adherence_percent")) for d in docs]
        if len(adherence_values) < 3:
            continue

        goal_code = _goal_to_code(user_goal.get(email, "maintenance"))

        for i in range(2, len(adherence_values)):
            history = adherence_values[:i]
            next_adherence = adherence_values[i]

            avg_adherence = float(sum(history) / len(history))
            adherence_std = float(pd.Series(history).std(ddof=0)) if len(history) > 1 else 0.0
            adherence_trend = float(history[-1] - history[0]) if len(history) > 1 else 0.0
            target_success = int(next_adherence >= 70.0)

            rows.append(
                {
                    "avg_adherence": avg_adherence,
                    "adherence_std": adherence_std,
                    "adherence_count": float(len(history)),
                    "adherence_trend": adherence_trend,
                    "goal_code": float(goal_code),
                    "target_success": target_success,
                }
            )

    return rows


def _generate_synthetic_goal_rows(n_rows: int = 800) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(42)
    rows: List[Dict[str, Any]] = []

    for _ in range(n_rows):
        goal_code = int(rng.integers(0, 4))
        adherence_count = float(rng.integers(3, 20))
        avg_adherence = float(np.clip(rng.normal(68, 16), 25, 98))
        adherence_std = float(np.clip(rng.normal(10, 5), 0, 30))
        adherence_trend = float(np.clip(rng.normal(2, 10), -25, 25))

        logit = (
            -5.5
            + 0.08 * avg_adherence
            - 0.03 * adherence_std
            + 0.015 * adherence_count
            + 0.02 * adherence_trend
            + (0.2 if goal_code == 0 else 0.0)
        )
        prob = 1.0 / (1.0 + np.exp(-logit))
        target_success = int(rng.random() < prob)

        rows.append(
            {
                "avg_adherence": avg_adherence,
                "adherence_std": adherence_std,
                "adherence_count": adherence_count,
                "adherence_trend": adherence_trend,
                "goal_code": float(goal_code),
                "target_success": target_success,
            }
        )

    return rows


def _extract_meal_training_rows(db) -> List[Dict[str, Any]]:
    feedback_docs = list(
        db["plan_feedback"]
        .find(
            {},
            {
                "email": 1,
                "adherence_percent": 1,
                "energy_rating": 1,
                "feedback_text": 1,
                "created_at": 1,
            },
        )
        .sort([("email", 1), ("created_at", 1)])
    )

    per_user_count: Dict[str, int] = {}
    rows: List[Dict[str, Any]] = []

    for doc in feedback_docs:
        email = str(doc.get("email", "")).strip().lower()
        if not email:
            continue

        per_user_count[email] = per_user_count.get(email, 0) + 1

        text = str(doc.get("feedback_text", "") or "")
        avg_user_rating = _safe_float(doc.get("energy_rating"), 3.0)

        rows.append(
            {
                "avg_user_rating": avg_user_rating,
                "history_count": float(per_user_count[email]),
                "has_high_protein": float(_contains_any(text, ["chicken", "paneer", "dal", "egg", "fish", "soy"])),
                "has_veg": float(_contains_any(text, ["salad", "vegetable", "sabzi", "greens"])),
                "is_fried": float(_contains_any(text, ["fried", "pakora", "bhatura", "chips"])),
                "spice_heavy": float(_contains_any(text, ["very spicy", "spicy", "masala"])),
                "text_len": float(len(text)),
                "target_adherence": int(_safe_float(doc.get("adherence_percent")) >= 70.0),
            }
        )

    return rows


def _generate_synthetic_meal_rows(n_rows: int = 1000) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(77)
    rows: List[Dict[str, Any]] = []

    for _ in range(n_rows):
        avg_user_rating = float(np.clip(rng.normal(3.4, 0.8), 1.0, 5.0))
        history_count = float(rng.integers(1, 40))
        has_high_protein = float(rng.integers(0, 2))
        has_veg = float(rng.integers(0, 2))
        is_fried = float(rng.integers(0, 2))
        spice_heavy = float(rng.integers(0, 2))
        text_len = float(rng.integers(10, 160))

        logit = (
            -0.8
            + 0.7 * (avg_user_rating - 3.0)
            + 0.2 * has_high_protein
            + 0.15 * has_veg
            - 0.28 * is_fried
            - 0.12 * spice_heavy
            + 0.01 * min(history_count, 20)
        )
        prob = 1.0 / (1.0 + np.exp(-logit))
        target_adherence = int(rng.random() < prob)

        rows.append(
            {
                "avg_user_rating": avg_user_rating,
                "history_count": history_count,
                "has_high_protein": has_high_protein,
                "has_veg": has_veg,
                "is_fried": is_fried,
                "spice_heavy": spice_heavy,
                "text_len": text_len,
                "target_adherence": target_adherence,
            }
        )

    return rows


def main() -> None:
    output_dir = os.path.join(PROJECT_ROOT, "data", "training")
    os.makedirs(output_dir, exist_ok=True)

    db = connect_to_mongo()
    try:
        goal_rows = _extract_goal_training_rows(db)
        meal_rows = _extract_meal_training_rows(db)

        # Cold-start safety: bootstrap synthetic rows when historical data is not enough yet.
        if len(goal_rows) < 100:
            goal_rows.extend(_generate_synthetic_goal_rows(1000 - len(goal_rows)))

        if len(meal_rows) < 100:
            meal_rows.extend(_generate_synthetic_meal_rows(1200 - len(meal_rows)))

        goal_df = pd.DataFrame(
            goal_rows,
            columns=[
                "avg_adherence",
                "adherence_std",
                "adherence_count",
                "adherence_trend",
                "goal_code",
                "target_success",
            ],
        )
        meal_df = pd.DataFrame(
            meal_rows,
            columns=[
                "avg_user_rating",
                "history_count",
                "has_high_protein",
                "has_veg",
                "is_fried",
                "spice_heavy",
                "text_len",
                "target_adherence",
            ],
        )

        goal_path = os.path.join(output_dir, "goal_achievement_training.csv")
        meal_path = os.path.join(output_dir, "meal_adherence_training.csv")

        goal_df.to_csv(goal_path, index=False)
        meal_df.to_csv(meal_path, index=False)

        print("Export complete")
        print(f"goal rows: {len(goal_df)} -> {goal_path}")
        print(f"meal rows: {len(meal_df)} -> {meal_path}")
    finally:
        close_mongo_connection()


if __name__ == "__main__":
    main()
