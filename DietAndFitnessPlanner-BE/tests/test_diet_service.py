import unittest

from app.services.dietService import IndianDietService


class DietServiceTests(unittest.TestCase):
    def test_muscle_gain_with_lower_target_weight_uses_deficit_and_high_protein(self):
        plan = IndianDietService.generate_indian_meal_plan(
            name="Asha",
            age=22,
            weight=75,
            height_cm=175,
            fitness_level="moderate",
            goal="muscle_gain",
            budget_preference="value",
            diet_type="veg",
            target_weight=70,
        )

        self.assertLessEqual(plan["daily_targets"]["calories"], 2150)
        self.assertGreaterEqual(plan["daily_targets"]["protein"], 140)


if __name__ == "__main__":
    unittest.main()
