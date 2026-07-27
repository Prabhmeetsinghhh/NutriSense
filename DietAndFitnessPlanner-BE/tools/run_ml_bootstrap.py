import os
import subprocess
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)


def _run(script_name: str) -> None:
    script_path = os.path.join(CURRENT_DIR, script_name)
    cmd = [sys.executable, script_path]
    print(f"\n>>> Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)


def main() -> None:
    _run("export_ml_training_data.py")
    _run("train_goal_achievement_model.py")
    _run("train_meal_adherence_model.py")
    food_dataset_dir = os.path.join(PROJECT_ROOT, "data", "food_images")
    if os.path.exists(food_dataset_dir):
        _run("train_food_classifier.py")
    else:
        print("\n>>> Skipping food classifier training (data/food_images not found)")
    _run("smoke_test_ml_pipeline.py")
    print("\nML bootstrap completed successfully")


if __name__ == "__main__":
    main()
