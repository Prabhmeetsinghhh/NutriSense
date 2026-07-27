import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.services.mlService import (  # noqa: E402
    goal_achievement_service,
    meal_optimization_service,
)


def main() -> None:
    goal_result = goal_achievement_service.predict_goal_achievement(
        email="smoke@test.com",
        goal="weight_loss",
        adherence_history=[62, 68, 71, 74, 80],
    )

    meal_score = meal_optimization_service.predict_meal_adherence(
        email="smoke@test.com",
        proposed_meal="grilled chicken with dal and salad",
        user_history=[{"rating": 4}, {"rating": 5}, {"rating": 4}],
    )

    assert 0.0 <= float(goal_result.get("success_probability", 0.0)) <= 1.0
    assert 0.0 <= float(meal_score) <= 1.0

    print("Smoke tests passed")
    print("goal_result:", goal_result)
    print("meal_score:", meal_score)


if __name__ == "__main__":
    main()
