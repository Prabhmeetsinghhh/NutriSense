import json
import os
import sys
from datetime import datetime

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


def main() -> None:
    data_path = os.path.join(PROJECT_ROOT, "data", "training", "meal_adherence_training.csv")
    model_dir = os.path.join(PROJECT_ROOT, "models")
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Training file not found: {data_path}")

    df = pd.read_csv(data_path)
    if len(df) < 50:
        raise ValueError("Not enough data to train meal adherence model. Need at least 50 rows.")

    feature_order = [
        "avg_user_rating",
        "history_count",
        "has_high_protein",
        "has_veg",
        "is_fried",
        "spice_heavy",
        "text_len",
    ]
    target_col = "target_adherence"

    missing = [c for c in feature_order + [target_col] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    x = df[feature_order].fillna(0.0)
    y = df[target_col].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = GradientBoostingClassifier(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=3,
        random_state=42,
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)) if len(set(y_test)) > 1 else None,
        "n_rows": int(len(df)),
        "trained_at": datetime.utcnow().isoformat() + "Z",
    }

    artifact = {
        "model": model,
        "feature_order": feature_order,
        "metrics": metrics,
        "model_name": "meal_adherence_model",
    }

    model_path = os.path.join(model_dir, "meal_adherence_model.joblib")
    metrics_path = os.path.join(model_dir, "meal_adherence_model.metrics.json")

    joblib.dump(artifact, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Meal adherence model trained successfully")
    print(f"model: {model_path}")
    print(f"metrics: {metrics_path}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
