from typing import List, Dict, Any, Tuple
import copy
from app.models.indianFoods import (
    INDIAN_BREAKFAST_OPTIONS,
    INDIAN_LUNCH_OPTIONS,
    INDIAN_SNACKS_OPTIONS,
    INDIAN_DINNER_OPTIONS,
    PROTEIN_BOOSTERS,
    BUDGET_TIERS
)

class IndianDietService:
    """
    Indian Diet Service - Creates personalized meal plans for:
    - College students
    - Hostel dwellers
    - Budget-conscious professionals
    - Fitness enthusiasts in India
    """

    @staticmethod
    def calculate_tdee(weight: int, height_cm: int, age: int, fitness_level: str) -> int:
        """
        Calculate Total Daily Energy Expenditure using Mifflin-St Jeor equation
        """
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5

        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }

        tdee = bmr * activity_multipliers.get(fitness_level, 1.55)
        return int(tdee)

    @staticmethod
    def calculate_bmi(weight: int, height_cm: int) -> float:
        """
        Calculate BMI = weight (kg) / (height (m))^2
        """
        height_m = height_cm / 100
        return weight / (height_m ** 2)

    @staticmethod
    def get_goal_from_bmi(bmi: float) -> str:
        """
        Map BMI to goal:
        BMI < 18.5 → Bulking Diet (muscle_gain)
        BMI 18.5–24.9 → Maintenance
        BMI > 25 → Fat Loss Diet (weight_loss)
        """
        if bmi < 18.5:
            return "muscle_gain"
        elif bmi > 25:
            return "weight_loss"
        else:
            return "maintenance"

    @staticmethod
    def calculate_protein_requirement(weight: int, experience: str) -> float:
        """
        Calculate daily protein requirement based on experience level
        Beginner → 1.2 g protein × bodyweight
        Intermediate → 1.5 g protein × bodyweight
        Advanced → 1.8 g protein × bodyweight
        """
        multipliers = {
            "beginner": 1.2,
            "intermediate": 1.5,
            "advanced": 1.8
        }
        return weight * multipliers.get(experience.lower(), 1.5)

    @staticmethod
    def get_meal_templates(diet_preference: str) -> Dict[str, Dict[str, Any]]:
        """
        Get meal templates based on diet preference
        """
        templates = {
            "veg": {
                "breakfast": {
                    "name": "Oats with Milk and Fruits",
                    "items": ["Oats (50g)", "Milk (250ml)", "Peanut Butter (1 tbsp)", "5 Almonds", "1 Banana"],
                    "protein": 15,
                    "calories": 350
                },
                "lunch": {
                    "name": "Dal Rice with Vegetables",
                    "items": ["Rice (100g)", "Dal (100g)", "Mixed Vegetables", "2 Roti"],
                    "protein": 20,
                    "calories": 450
                },
                "evening": {
                    "name": "Fruit and Nuts",
                    "items": ["1 Apple", "Handful of Nuts", "Green Tea"],
                    "protein": 8,
                    "calories": 200
                },
                "dinner": {
                    "name": "Vegetable Curry with Roti",
                    "items": ["2 Roti", "Vegetable Curry", "Salad"],
                    "protein": 15,
                    "calories": 400
                }
            },
            "non_veg": {
                "breakfast": {
                    "name": "Eggs with Bread and Milk",
                    "items": ["3 Eggs", "2 Bread slices", "Milk (200ml)", "1 Banana"],
                    "protein": 25,
                    "calories": 380
                },
                "lunch": {
                    "name": "Chicken with Rice and Vegetables",
                    "items": ["Rice (100g)", "Chicken (150g)", "Mixed Vegetables", "2 Roti"],
                    "protein": 35,
                    "calories": 500
                },
                "evening": {
                    "name": "Boiled Eggs and Fruit",
                    "items": ["2 Boiled Eggs", "1 Orange", "Handful of Peanuts"],
                    "protein": 15,
                    "calories": 250
                },
                "dinner": {
                    "name": "Fish with Roti and Vegetables",
                    "items": ["Fish (200g)", "2 Roti", "Mixed Vegetables"],
                    "protein": 40,
                    "calories": 450
                }
            },
            "vegan": {
                "breakfast": {
                    "name": "Tofu Scramble with Quinoa",
                    "items": ["Tofu (150g)", "Quinoa (50g)", "Mixed Vegetables"],
                    "protein": 18,
                    "calories": 320
                },
                "lunch": {
                    "name": "Brown Rice with Lentils",
                    "items": ["Brown Rice (100g)", "Lentils (100g)", "Mixed Vegetables"],
                    "protein": 22,
                    "calories": 420
                },
                "evening": {
                    "name": "Nuts and Dried Fruits",
                    "items": ["Mixed Nuts (30g)", "Dried Fruits", "Green Smoothie"],
                    "protein": 10,
                    "calories": 280
                },
                "dinner": {
                    "name": "Tofu Stir Fry with Rice",
                    "items": ["Tofu (150g)", "Brown Rice (100g)", "Stir Fried Vegetables"],
                    "protein": 20,
                    "calories": 380
                }
            },
            "eggetarian": {
                "breakfast": {
                    "name": "Eggs with Roti and Vegetables",
                    "items": ["3 Eggs", "2 Roti", "Mixed Vegetables"],
                    "protein": 22,
                    "calories": 360
                },
                "lunch": {
                    "name": "Egg Curry with Rice",
                    "items": ["Rice (100g)", "Egg Curry (3 eggs)", "Mixed Vegetables"],
                    "protein": 28,
                    "calories": 480
                },
                "evening": {
                    "name": "Boiled Eggs and Salad",
                    "items": ["2 Boiled Eggs", "Fresh Salad", "Fruit"],
                    "protein": 14,
                    "calories": 220
                },
                "dinner": {
                    "name": "Omelette with Roti",
                    "items": ["3 Egg Omelette", "2 Roti", "Vegetable Salad"],
                    "protein": 25,
                    "calories": 420
                }
            }
        }
        return templates.get(diet_preference.lower(), templates["veg"])

    @staticmethod
    def generate_rule_based_meal_plan(
        name: str,
        age: int,
        weight: int,
        height_cm: int,
        experience: str,
        diet_preference: str,
        budget_preference: str = "value",
    ) -> Dict[str, Any]:
        """
        Generate rule-based meal plan following the specified logic
        """
        # Calculate BMI and determine goal
        bmi = IndianDietService.calculate_bmi(weight, height_cm)
        goal = IndianDietService.get_goal_from_bmi(bmi)
        
        # Map experience to fitness level for TDEE calculation
        fitness_level_mapping = {
            "beginner": "light",
            "intermediate": "moderate",
            "advanced": "active"
        }
        fitness_level = fitness_level_mapping.get(experience.lower(), "moderate")
        
        # Calculate protein requirement
        total_protein = IndianDietService.calculate_protein_requirement(weight, experience)
        
        # Calculate TDEE for calorie targets
        tdee = IndianDietService.calculate_tdee(weight, height_cm, age, fitness_level)
        
        # Divide protein across meals (25% breakfast, 30% lunch, 20% evening, 25% dinner)
        protein_distribution = {
            "breakfast": total_protein * 0.25,
            "lunch": total_protein * 0.30,
            "evening": total_protein * 0.20,
            "dinner": total_protein * 0.25
        }
        
        # Get meal templates
        templates = IndianDietService.get_meal_templates(diet_preference)
        budget_tier_key = IndianDietService.get_budget_tier(budget_preference)
        tier_info = BUDGET_TIERS.get(budget_tier_key, BUDGET_TIERS["value"])
        meal_cost_range = tier_info.get("meal_cost", "₹75-100")
        
        # Generate meal plan
        daily_plan = {}
        total_calories = 0
        total_protein_actual = 0
        
        for meal_time, protein_target in protein_distribution.items():
            meal_template = templates[meal_time]
            daily_plan[meal_time] = {
                "name": meal_template["name"],
                "portion": ", ".join(meal_template["items"]),
                "protein": round(protein_target, 1),
                "calories": meal_template["calories"],
                "macros": {
                    "protein": round(protein_target, 1),
                    "carbs": round(meal_template["calories"] * 0.5 / 4, 1),  # Estimate carbs
                    "fat": round(meal_template["calories"] * 0.2 / 9, 1)     # Estimate fat
                },
                "cost": meal_cost_range,
                "prep_time": "15-20 mins",
                "availability": "Common"
            }
            total_calories += meal_template["calories"]
            total_protein_actual += protein_target
        
        # Adjust calories based on goal
        if goal == "muscle_gain":
            target_calories = tdee + 300
        elif goal == "weight_loss":
            target_calories = tdee - 500
        else:
            target_calories = tdee
        
        return {
            "user_name": name,
            "bmi": round(bmi, 1),
            "goal": goal,
            "experience": experience,
            "diet_preference": diet_preference,
            "daily_plan": daily_plan,
            "daily_totals": {
                "calories": total_calories,
                "protein": round(total_protein_actual, 1),
                "carbs": round(sum(m["macros"]["carbs"] for m in daily_plan.values()), 1),
                "fat": round(sum(m["macros"]["fat"] for m in daily_plan.values()), 1)
            },
            "daily_targets": {
                "calories": target_calories,
                "protein": round(total_protein, 1),
                "carbs": round(target_calories * 0.5 / 4, 1),
                "fat": round(target_calories * 0.2 / 9, 1)
            },
            "budget_tier": {
                "name": tier_info["name"],
                "emoji": tier_info["emoji"],
                "description": tier_info["description"]
            },
            "hydration": "3-4 liters daily",
            "diet_tips": [
                f"Your BMI is {round(bmi, 1)} - {goal.replace('_', ' ').title()} recommended",
                f"Aim for {round(total_protein, 1)}g protein daily",
                "Stay hydrated throughout the day",
                "Include variety in your meals",
                "Consult a doctor before major dietary changes"
            ],
            "disclaimer": "This is a general recommendation. Consult a nutritionist for personalized advice"
        }

    @staticmethod
    def calculate_macros(tdee: int, goal: str, weight: int) -> Dict[str, float]:
        """
        Calculate daily macro targets based on goal
        """
        macros = {}

        if goal == "muscle_gain":
            # High protein for muscle building
            macros["protein_percent"] = 0.30
            macros["carbs_percent"] = 0.50
            macros["fat_percent"] = 0.20
            macros["protein_g_per_kg"] = 1.8
        elif goal == "weight_loss":
            # Higher protein, lower carbs
            macros["protein_percent"] = 0.35
            macros["carbs_percent"] = 0.40
            macros["fat_percent"] = 0.20
            macros["protein_g_per_kg"] = 2.0
        elif goal == "maintenance":
            # Balanced macros
            macros["protein_percent"] = 0.28
            macros["carbs_percent"] = 0.50
            macros["fat_percent"] = 0.22
            macros["protein_g_per_kg"] = 1.65
        elif goal == "muscle_endurance":
            # Moderate protein, high carbs
            macros["protein_percent"] = 0.28
            macros["carbs_percent"] = 0.60
            macros["fat_percent"] = 0.12
            macros["protein_g_per_kg"] = 1.8

        # Calculate absolute values
        macros["protein_g"] = weight * macros["protein_g_per_kg"]
        macros["protein_cal"] = macros["protein_g"] * 4
        
        macros["carbs_cal"] = tdee * macros["carbs_percent"]
        macros["carbs_g"] = macros["carbs_cal"] / 4

        macros["fat_cal"] = tdee * macros["fat_percent"]
        macros["fat_g"] = macros["fat_cal"] / 9

        return macros

    @staticmethod
    def get_budget_tier(budget_preference: str) -> str:
        """
        Determine budget tier - returns the tier key
        """
        mapping = {
            # New slab keys from frontend
            "affordable": "affordable",
            "value": "value",
            "balanced": "balanced",
            "premium": "premium",
            # Backward-compatible keys
            "budget": "value",
            "moderate": "balanced",
        }
        return mapping.get((budget_preference or "").lower(), "value")

    @staticmethod
    def _parse_cost_string(cost_str: str) -> float:
        """Convert a price string like '₹30-40' or '₹60' to a numeric average."""
        try:
            # remove currency symbol and split ranges
            cleaned = cost_str.replace('₹', '').replace('Rs.', '').strip()
            if '-' in cleaned:
                parts = cleaned.split('-')
                nums = [float(p) for p in parts if p]
                return sum(nums) / len(nums)
            return float(cleaned)
        except Exception:
            return 0.0

    def find_best_meal_combination(
        available_calories: int,
        protein_needed: float,
        carbs_target: float,
        fat_target: float,
        meal_type: str,
        budget_tier: str,
        used_foods: List[str] = None,
        diet_type: str = "veg"
    ) -> Dict[str, Any]:
        """
        Find the best meal combination to meet nutritional targets
        """
        if used_foods is None:
            used_foods = []

        # Select food options based on meal type and budget
        if meal_type == "breakfast":
            food_options = INDIAN_BREAKFAST_OPTIONS
        elif meal_type == "lunch":
            food_options = INDIAN_LUNCH_OPTIONS
        elif meal_type == "snack":
            food_options = INDIAN_SNACKS_OPTIONS
        else:  # dinner
            food_options = INDIAN_DINNER_OPTIONS

        # Filter by budget tier preference
        best_meals = []
        tier_preference = BUDGET_TIERS[budget_tier]["foods"]

        # Sort foods by how well they fit the calorie target
        for food_key, food_data in food_options.items():
            if food_key in used_foods:
                continue

            # Filter by diet type - handle both veg_egg as a diet type or as part of eggetarian
            food_diet_types = food_data.get("diet_type", [])
            if diet_type not in food_diet_types:
                continue

            # Calculate how close this meal gets us to targets
            cal_diff = abs(food_data["calories"] - available_calories)
            protein_score = min(food_data["protein"], protein_needed)

            # Prefer foods that match budget tier
            tier_score = 5 if food_key in tier_preference else 0

            # incorporate cost sensitivity to push budgets apart
            cost_val = IndianDietService._parse_cost_string(food_data.get("cost", "0"))
            cost_score = 0
            if budget_tier == "affordable":
                # Strongly penalize expensive foods in lowest range
                cost_score = cost_val * 0.8
            elif budget_tier in ["value", "budget"]:
                # Moderate penalty for budget-friendly range
                cost_score = cost_val * 0.45
            elif budget_tier in ["balanced", "moderate"]:
                # Mild penalty for mid-tier range
                cost_score = cost_val * 0.2
            elif budget_tier == "premium":
                # reward expensive items (negative score)
                cost_score = -cost_val * 0.5

            # Calculate overall match score (lower is better)
            match_score = cal_diff + (20 - protein_score * 2) - tier_score + cost_score

            best_meals.append({
                "key": food_key,
                "score": match_score,
                **food_data,
                "_cost_numeric": cost_val
            })

        best_meals.sort(key=lambda x: x["score"])

        # Add some randomization to avoid always picking the same food
        import random
        if len(best_meals) > 2:
            # Take top 3 and pick randomly to ensure variety
            top_candidates = best_meals[:3]
            selected = random.choice(top_candidates)
        elif best_meals:
            selected = best_meals[0]
        else:
            return None

        remaining_protein = max(0, protein_needed - selected["protein"])

        # include cost numeric for later aggregation
        return {
            "meal": {
                "name": selected["name"],
                "portion": selected["portion"],
                "calories": selected["calories"],
                "protein": selected["protein"],
                "carbs": selected["carbs"],
                "fat": selected["fat"],
                "cost": selected["cost"],
                "_cost_numeric": selected.get("_cost_numeric", 0),
                "prep_time": selected.get("prep_time"),
                "availability": selected.get("availability")
            },
            "remaining_protein": remaining_protein,
            "key": selected["key"]
        }

        return None

    @staticmethod
    def add_protein_booster(
        current_protein: float,
        protein_needed: float,
        budget_tier: str,
        diet_type: str = "veg"
    ) -> Dict[str, Any]:
        """
        Add protein boosters if meal doesn't meet protein targets
        """
        if current_protein >= protein_needed * 0.9:  # Already close enough
            return None

        protein_deficit = protein_needed - current_protein

        # Filter boosters based on budget and diet type
        if budget_tier in ["affordable", "value", "budget"]:
            # Cheapest options: eggs, curd, dal
            boosters = {k: v for k, v in PROTEIN_BOOSTERS.items() 
                       if k in ["egg", "curd", "moong_dal"] and diet_type in v.get("diet_type", [])}
        else:
            # All options available for the diet type
            boosters = {k: v for k, v in PROTEIN_BOOSTERS.items() 
                       if diet_type in v.get("diet_type", [])}

        # Find best booster
        best_booster = None
        best_score = float('inf')

        for booster_key, booster_data in boosters.items():
            # Score based on protein content and cost efficiency
            protein_score = booster_data["protein"]
            cost_factor = 100  # Base factor for cost comparison

            score = abs(protein_score - protein_deficit) + (cost_factor if "₹" in booster_data["cost"] else 0)

            if score < best_score:
                best_score = score
                best_booster = {
                    "name": booster_data["name"],
                    "portion": booster_data["portion"],
                    "calories": booster_data["calories"],
                    "protein": booster_data["protein"],
                    "carbs": booster_data["carbs"],
                    "fat": booster_data["fat"],
                    "cost": booster_data["cost"],
                    "reason": f"Add this to reach {protein_needed}g protein target"
                }

        return best_booster

    @staticmethod
    def generate_indian_meal_plan(
        name: str,
        age: int,
        weight: int,
        height_cm: int,
        fitness_level: str,
        goal: str,
        budget_preference: str = "moderate",
        diet_type: str = "veg"
    ) -> Dict[str, Any]:
        """
        Generate complete daily meal plan for Indian user.
        Structure is fixed to 4 meals and optimized for hostel/mess practicality,
        goal adaptation, and budget control.
        """
        budget_tier = IndianDietService.get_budget_tier(budget_preference)
        maintenance_calories = IndianDietService.calculate_tdee(weight, height_cm, age, fitness_level)
        protein_min, protein_max = IndianDietService._goal_protein_range(goal, weight)
        target_protein = round((protein_min + protein_max) / 2, 1)
        target_calories = IndianDietService._goal_calorie_target(goal, maintenance_calories)

        # Fixed 4-meal structure with hostel/mess-friendly options.
        daily_plan = IndianDietService._get_structured_hostel_plan(budget_tier, diet_type)
        adjustment_notes = IndianDietService._apply_goal_adjustments(daily_plan, goal, diet_type)

        daily_totals = {
            "calories": round(sum(m.get("calories", 0) for m in daily_plan.values()), 1),
            "protein": round(sum(m.get("protein", 0) for m in daily_plan.values()), 1),
            "carbs": round(sum(m.get("carbs", 0) for m in daily_plan.values()), 1),
            "fat": round(sum(m.get("fat", 0) for m in daily_plan.values()), 1),
        }

        # Try one practical booster when protein is under target range.
        if daily_totals["protein"] < protein_min:
            booster = IndianDietService._select_goal_booster(diet_type, budget_tier)
            if booster:
                dinner = daily_plan.get("dinner", {})
                dinner["protein_booster"] = {
                    "name": booster["name"],
                    "portion": booster["portion"],
                    "calories": booster["calories"],
                    "protein": booster["protein"],
                    "carbs": booster["carbs"],
                    "fat": booster["fat"],
                    "cost": booster["cost"],
                    "reason": f"Added to improve protein coverage towards {round(protein_min, 1)}-{round(protein_max, 1)}g/day"
                }
                dinner["calories"] += booster["calories"]
                dinner["protein"] += booster["protein"]
                dinner["carbs"] += booster["carbs"]
                dinner["fat"] += booster["fat"]

                daily_totals = {
                    "calories": round(sum(m.get("calories", 0) for m in daily_plan.values()), 1),
                    "protein": round(sum(m.get("protein", 0) for m in daily_plan.values()), 1),
                    "carbs": round(sum(m.get("carbs", 0) for m in daily_plan.values()), 1),
                    "fat": round(sum(m.get("fat", 0) for m in daily_plan.values()), 1),
                }
                adjustment_notes.append(f"Added protein booster in dinner: {booster['name']} ({booster['portion']}).")

        tier_info = BUDGET_TIERS[budget_tier]
        diet_tips = IndianDietService.get_diet_tips(goal, budget_tier, weight)

        if daily_totals["protein"] < protein_min:
            diet_tips.append(
                f"Current structure gives ~{daily_totals['protein']}g protein. Target range for your goal is {round(protein_min, 1)}-{round(protein_max, 1)}g/day."
            )
            diet_tips.append("In this budget tier, use swap system: paneer/chicken/eggs/soya and add one extra high-protein serving.")

        if adjustment_notes:
            diet_tips.extend(adjustment_notes)

        carb_ratio = 0.68 if goal == "weight_loss" else (0.72 if goal == "muscle_gain" else 0.70)
        protein_calories = target_protein * 4
        remaining_cals = max(0, target_calories - protein_calories)
        target_carbs = round((remaining_cals * carb_ratio) / 4, 1)
        target_fat = round((remaining_cals * (1 - carb_ratio)) / 9, 1)

        return {
            "user_name": name,
            "daily_plan": daily_plan,
            "daily_totals": daily_totals,
            "daily_targets": {
                "calories": target_calories,
                "protein": target_protein,
                "carbs": target_carbs,
                "fat": target_fat,
            },
            "budget_tier": {
                "name": tier_info["name"],
                "emoji": tier_info["emoji"],
                "description": tier_info["description"],
            },
            "hydration": "3-4 liters daily (adjust based on activity)",
            "diet_tips": diet_tips,
            "disclaimer": "Consult a nutritionist for personalized advice"
        }

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> int:
        return int(max(minimum, min(maximum, value)))

    @staticmethod
    def _goal_protein_range(goal: str, weight: int) -> Tuple[float, float]:
        mapping = {
            "weight_loss": (1.8, 2.2),
            "maintenance": (1.5, 1.8),
            "muscle_gain": (1.6, 2.0),
            "muscle_endurance": (1.6, 1.9),
        }
        low, high = mapping.get(goal, mapping["maintenance"])
        return weight * low, weight * high

    @staticmethod
    def _goal_calorie_target(goal: str, maintenance_calories: int) -> int:
        ranges = {
            "weight_loss": (1800, 2200, -350),
            "maintenance": (2200, 2600, 0),
            "muscle_gain": (2600, 3000, 300),
            "muscle_endurance": (2400, 2800, 150),
        }
        low, high, delta = ranges.get(goal, ranges["maintenance"])
        return IndianDietService._clamp(maintenance_calories + delta, low, high)

    @staticmethod
    def _get_structured_hostel_plan(budget_tier: str, diet_type: str) -> Dict[str, Dict[str, Any]]:
        key = diet_type if diet_type in ["veg", "non_veg", "vegan", "veg_egg"] else "veg"

        plans: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {
            "affordable": {
                "veg": {
                    "breakfast": {"name": "Banana + Milk + Peanuts", "portion": "2 bananas, 250ml milk, 20g peanuts", "calories": 350, "protein": 12, "carbs": 52, "fat": 10, "cost": "₹30", "prep_time": "5 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Roti + Dal + Sabzi", "portion": "3 roti, 1 bowl dal, 1 bowl sabzi", "calories": 500, "protein": 18, "carbs": 75, "fat": 12, "cost": "₹50", "prep_time": "Mess ready", "availability": "Mess"},
                    "snack": {"name": "Roasted Chana + Chai", "portion": "50g roasted chana, 1 cup chai", "calories": 200, "protein": 10, "carbs": 24, "fat": 5, "cost": "₹20", "prep_time": "2 mins", "availability": "Everywhere"},
                    "dinner": {"name": "Mess Roti + Dal + Paneer", "portion": "3 roti, 1 bowl dal, 50g paneer", "calories": 550, "protein": 25, "carbs": 62, "fat": 18, "cost": "₹80", "prep_time": "Mess + add-on", "availability": "Hostel + local dairy"},
                },
                "non_veg": {
                    "breakfast": {"name": "Eggs + Bread + Chai", "portion": "2 eggs, 2 bread slices, 1 chai", "calories": 350, "protein": 14, "carbs": 34, "fat": 16, "cost": "₹35", "prep_time": "8 mins", "availability": "Hostel canteen"},
                    "lunch": {"name": "Mess Roti + Dal", "portion": "3 roti, 1 bowl dal", "calories": 500, "protein": 15, "carbs": 72, "fat": 11, "cost": "₹50", "prep_time": "Mess ready", "availability": "Mess"},
                    "snack": {"name": "Boiled Eggs", "portion": "3 boiled eggs", "calories": 220, "protein": 18, "carbs": 2, "fat": 15, "cost": "₹30", "prep_time": "5 mins", "availability": "Everywhere"},
                    "dinner": {"name": "Chicken + Roti", "portion": "150g chicken curry, 2 roti", "calories": 730, "protein": 35, "carbs": 58, "fat": 26, "cost": "₹120", "prep_time": "20 mins", "availability": "Outside mess/dhaba"},
                },
                "vegan": {
                    "breakfast": {"name": "Banana + Peanuts", "portion": "2 bananas, 25g peanuts", "calories": 300, "protein": 10, "carbs": 42, "fat": 12, "cost": "₹25", "prep_time": "2 mins", "availability": "Everywhere"},
                    "lunch": {"name": "Mess Roti + Dal + Sabzi", "portion": "3 roti, 1 bowl dal, 1 bowl sabzi", "calories": 480, "protein": 15, "carbs": 74, "fat": 11, "cost": "₹50", "prep_time": "Mess ready", "availability": "Mess"},
                    "snack": {"name": "Roasted Chana", "portion": "50g roasted chana", "calories": 180, "protein": 10, "carbs": 24, "fat": 3, "cost": "₹20", "prep_time": "1 min", "availability": "Everywhere"},
                    "dinner": {"name": "Soya Chunks + Roti", "portion": "50g dry soya chunks, 2 roti", "calories": 600, "protein": 25, "carbs": 68, "fat": 16, "cost": "₹75", "prep_time": "15 mins", "availability": "Hostel pantry friendly"},
                },
                "veg_egg": {
                    "breakfast": {"name": "Eggs + Banana + Milk", "portion": "2 eggs, 1 banana, 250ml milk", "calories": 420, "protein": 24, "carbs": 35, "fat": 18, "cost": "₹45", "prep_time": "8 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Roti + Dal", "portion": "3 roti, 1 bowl dal", "calories": 500, "protein": 16, "carbs": 72, "fat": 11, "cost": "₹50", "prep_time": "Mess ready", "availability": "Mess"},
                    "snack": {"name": "Boiled Eggs + Chana", "portion": "2 eggs, 30g roasted chana", "calories": 280, "protein": 22, "carbs": 14, "fat": 14, "cost": "₹35", "prep_time": "5 mins", "availability": "Everywhere"},
                    "dinner": {"name": "Roti + Dal + Paneer", "portion": "3 roti, 1 bowl dal, 50g paneer", "calories": 620, "protein": 30, "carbs": 66, "fat": 20, "cost": "₹80", "prep_time": "Mess + add-on", "availability": "Mess + local dairy"},
                },
            },
            "value": {
                "veg": {
                    "breakfast": {"name": "Oats + Milk + Banana", "portion": "50g oats, 250ml milk, 1 banana", "calories": 500, "protein": 20, "carbs": 68, "fat": 14, "cost": "₹60", "prep_time": "7 mins", "availability": "Hostel pantry"},
                    "lunch": {"name": "Mess Meal + Paneer Add-on", "portion": "3 roti, dal, sabzi, 100g paneer", "calories": 700, "protein": 35, "carbs": 78, "fat": 24, "cost": "₹95", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Peanut Butter Sandwich", "portion": "2 bread slices, 2 tbsp peanut butter", "calories": 380, "protein": 14, "carbs": 34, "fat": 20, "cost": "₹45", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Paneer Bhurji + Roti", "portion": "150g paneer bhurji, 2 roti", "calories": 700, "protein": 33, "carbs": 48, "fat": 32, "cost": "₹110", "prep_time": "20 mins", "availability": "Hostel + tiffin"},
                },
                "non_veg": {
                    "breakfast": {"name": "Eggs + Bread + Milk", "portion": "4 eggs, 2 bread slices, 200ml milk", "calories": 580, "protein": 30, "carbs": 34, "fat": 32, "cost": "₹70", "prep_time": "10 mins", "availability": "Hostel canteen"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 100g paneer", "calories": 650, "protein": 30, "carbs": 70, "fat": 22, "cost": "₹90", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Peanut Butter Sandwich", "portion": "2 bread slices, 2 tbsp peanut butter", "calories": 380, "protein": 12, "carbs": 34, "fat": 20, "cost": "₹40", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Chicken + Roti", "portion": "200g chicken, 2 roti", "calories": 790, "protein": 45, "carbs": 56, "fat": 28, "cost": "₹120", "prep_time": "20 mins", "availability": "Dhaba/tiffin"},
                },
                "vegan": {
                    "breakfast": {"name": "Oats + Banana + Peanuts", "portion": "60g oats, 1 banana, 20g peanuts", "calories": 520, "protein": 18, "carbs": 70, "fat": 18, "cost": "₹55", "prep_time": "6 mins", "availability": "Hostel pantry"},
                    "lunch": {"name": "Mess Meal + Soya", "portion": "3 roti, dal, sabzi, 40g dry soya chunks", "calories": 650, "protein": 30, "carbs": 84, "fat": 16, "cost": "₹85", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Roasted Chana + Fruit", "portion": "50g roasted chana, 1 seasonal fruit", "calories": 300, "protein": 13, "carbs": 48, "fat": 5, "cost": "₹35", "prep_time": "2 mins", "availability": "Everywhere"},
                    "dinner": {"name": "Soya Pulao", "portion": "60g dry soya chunks, rice, vegetables", "calories": 750, "protein": 40, "carbs": 92, "fat": 18, "cost": "₹110", "prep_time": "20 mins", "availability": "Hostel kitchen"},
                },
                "veg_egg": {
                    "breakfast": {"name": "Eggs + Oats + Milk", "portion": "3 eggs, 50g oats, 200ml milk", "calories": 580, "protein": 32, "carbs": 44, "fat": 26, "cost": "₹70", "prep_time": "10 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 100g paneer", "calories": 650, "protein": 30, "carbs": 70, "fat": 22, "cost": "₹90", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Egg Sandwich", "portion": "2 eggs, 2 bread slices", "calories": 360, "protein": 22, "carbs": 28, "fat": 18, "cost": "₹45", "prep_time": "7 mins", "availability": "Easy"},
                    "dinner": {"name": "Paneer + Egg Bhurji + Roti", "portion": "100g paneer, 2 eggs, 2 roti", "calories": 720, "protein": 36, "carbs": 46, "fat": 34, "cost": "₹110", "prep_time": "20 mins", "availability": "Hostel kitchen"},
                },
            },
            "balanced": {
                "veg": {
                    "breakfast": {"name": "Oats + Milk + Nuts", "portion": "60g oats, 300ml milk, 10g nuts", "calories": 560, "protein": 24, "carbs": 66, "fat": 20, "cost": "₹75", "prep_time": "8 mins", "availability": "Hostel pantry"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, sabzi, 120g paneer", "calories": 740, "protein": 38, "carbs": 78, "fat": 26, "cost": "₹100", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Peanut Butter Toast + Fruit", "portion": "2 toast, 2 tbsp peanut butter, fruit", "calories": 420, "protein": 15, "carbs": 45, "fat": 20, "cost": "₹50", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Paneer + Dal + Roti", "portion": "150g paneer, 1 bowl dal, 2 roti", "calories": 740, "protein": 37, "carbs": 52, "fat": 33, "cost": "₹115", "prep_time": "20 mins", "availability": "Hostel + tiffin"},
                },
                "non_veg": {
                    "breakfast": {"name": "Eggs + Oats + Milk", "portion": "4 eggs, 50g oats, 250ml milk", "calories": 620, "protein": 34, "carbs": 48, "fat": 28, "cost": "₹80", "prep_time": "10 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 100g paneer", "calories": 680, "protein": 32, "carbs": 72, "fat": 24, "cost": "₹95", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "PB Sandwich + Fruit", "portion": "2 bread slices, 2 tbsp peanut butter, fruit", "calories": 420, "protein": 14, "carbs": 46, "fat": 20, "cost": "₹50", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Chicken + Roti", "portion": "220g chicken, 2 roti", "calories": 830, "protein": 50, "carbs": 58, "fat": 30, "cost": "₹130", "prep_time": "20 mins", "availability": "Dhaba/tiffin"},
                },
                "vegan": {
                    "breakfast": {"name": "Oats + Peanut Shake", "portion": "60g oats, banana, 25g peanuts", "calories": 560, "protein": 20, "carbs": 72, "fat": 20, "cost": "₹65", "prep_time": "8 mins", "availability": "Hostel pantry"},
                    "lunch": {"name": "Mess Meal + Soya", "portion": "3 roti, dal, sabzi, 50g dry soya", "calories": 700, "protein": 34, "carbs": 88, "fat": 18, "cost": "₹90", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Chana + Fruit", "portion": "60g roasted chana, fruit", "calories": 330, "protein": 15, "carbs": 50, "fat": 6, "cost": "₹40", "prep_time": "2 mins", "availability": "Everywhere"},
                    "dinner": {"name": "Soya Rice Bowl", "portion": "70g dry soya, rice, vegetables", "calories": 800, "protein": 42, "carbs": 96, "fat": 20, "cost": "₹120", "prep_time": "20 mins", "availability": "Hostel kitchen"},
                },
                "veg_egg": {
                    "breakfast": {"name": "Eggs + Oats + Milk", "portion": "4 eggs, 50g oats, 250ml milk", "calories": 620, "protein": 36, "carbs": 46, "fat": 30, "cost": "₹80", "prep_time": "10 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 120g paneer", "calories": 700, "protein": 34, "carbs": 72, "fat": 25, "cost": "₹100", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "Egg Toast", "portion": "2 eggs, 2 toast, fruit", "calories": 400, "protein": 24, "carbs": 36, "fat": 16, "cost": "₹50", "prep_time": "7 mins", "availability": "Easy"},
                    "dinner": {"name": "Paneer + Egg Curry + Roti", "portion": "100g paneer, 2 eggs, 2 roti", "calories": 760, "protein": 38, "carbs": 48, "fat": 36, "cost": "₹120", "prep_time": "20 mins", "availability": "Hostel kitchen"},
                },
            },
            "premium": {
                "veg": {
                    "breakfast": {"name": "Oats + Milk + Nuts + Fruit", "portion": "70g oats, 300ml milk, nuts, fruit", "calories": 650, "protein": 26, "carbs": 78, "fat": 24, "cost": "₹90", "prep_time": "8 mins", "availability": "Easy"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, sabzi, 150g paneer", "calories": 780, "protein": 42, "carbs": 78, "fat": 30, "cost": "₹120", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "PB Banana Shake", "portion": "banana, 2 tbsp peanut butter, milk", "calories": 450, "protein": 16, "carbs": 42, "fat": 22, "cost": "₹60", "prep_time": "5 mins", "availability": "Hostel blender"},
                    "dinner": {"name": "Paneer + Dal + Rice", "portion": "200g paneer, dal, small rice", "calories": 860, "protein": 40, "carbs": 64, "fat": 40, "cost": "₹150", "prep_time": "25 mins", "availability": "Tiffin/kitchen"},
                },
                "non_veg": {
                    "breakfast": {"name": "Eggs + Oats + Milk", "portion": "5 eggs, oats, 250ml milk", "calories": 700, "protein": 40, "carbs": 50, "fat": 34, "cost": "₹95", "prep_time": "12 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 100g paneer", "calories": 680, "protein": 30, "carbs": 70, "fat": 24, "cost": "₹100", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "PB Banana Shake", "portion": "banana, peanut butter, milk", "calories": 450, "protein": 15, "carbs": 42, "fat": 22, "cost": "₹65", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Chicken + Roti", "portion": "250g chicken, 2 roti", "calories": 950, "protein": 55, "carbs": 64, "fat": 36, "cost": "₹160", "prep_time": "25 mins", "availability": "Dhaba/tiffin"},
                },
                "vegan": {
                    "breakfast": {"name": "Oats + Banana + Peanut Mix", "portion": "70g oats, banana, 25g peanuts", "calories": 640, "protein": 22, "carbs": 84, "fat": 24, "cost": "₹80", "prep_time": "8 mins", "availability": "Hostel pantry"},
                    "lunch": {"name": "Mess Meal + Soya", "portion": "3 roti, dal, sabzi, 60g dry soya", "calories": 760, "protein": 38, "carbs": 94, "fat": 20, "cost": "₹105", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "PB Sandwich + Fruit", "portion": "2 bread slices, peanut butter, fruit", "calories": 430, "protein": 14, "carbs": 46, "fat": 20, "cost": "₹55", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Soya Rice Bowl", "portion": "90g dry soya, rice, vegetables", "calories": 870, "protein": 46, "carbs": 102, "fat": 22, "cost": "₹140", "prep_time": "25 mins", "availability": "Hostel kitchen"},
                },
                "veg_egg": {
                    "breakfast": {"name": "Eggs + Oats + Milk", "portion": "5 eggs, oats, 250ml milk", "calories": 700, "protein": 42, "carbs": 48, "fat": 35, "cost": "₹95", "prep_time": "12 mins", "availability": "Hostel friendly"},
                    "lunch": {"name": "Mess Meal + Paneer", "portion": "3 roti, dal, 120g paneer", "calories": 710, "protein": 34, "carbs": 72, "fat": 26, "cost": "₹110", "prep_time": "Mess + add-on", "availability": "Mess"},
                    "snack": {"name": "PB Banana Shake", "portion": "banana, peanut butter, milk", "calories": 450, "protein": 15, "carbs": 42, "fat": 22, "cost": "₹60", "prep_time": "5 mins", "availability": "Easy"},
                    "dinner": {"name": "Paneer + Egg Curry + Roti", "portion": "150g paneer, 3 eggs, 2 roti", "calories": 900, "protein": 52, "carbs": 56, "fat": 44, "cost": "₹150", "prep_time": "25 mins", "availability": "Hostel kitchen"},
                },
            },
        }

        tier_plans = plans.get(budget_tier, plans["value"])
        diet_plans = tier_plans.get(key, tier_plans.get("veg", {}))
        return copy.deepcopy(diet_plans)

    @staticmethod
    def _apply_goal_adjustments(daily_plan: Dict[str, Dict[str, Any]], goal: str, diet_type: str) -> List[str]:
        notes: List[str] = []

        if goal == "weight_loss":
            dinner = daily_plan.get("dinner")
            if dinner:
                dinner["portion"] = f"{dinner.get('portion', '')}, reduce one carb serving (roti/rice)"
                dinner["calories"] = max(150, dinner.get("calories", 0) - 120)
                dinner["carbs"] = max(0, dinner.get("carbs", 0) - 22)
            notes.append("Fat loss mode: removed one carb source from dinner to create a practical deficit.")

        elif goal == "muscle_gain":
            snack = daily_plan.get("snack")
            if snack:
                snack["portion"] = f"{snack.get('portion', '')}, add banana + peanut butter"
                snack["calories"] += 220
                snack["protein"] += 8
                snack["carbs"] += 30
                snack["fat"] += 10
            notes.append("Muscle gain mode: added one carb and one fat source to increase recovery-friendly calories.")

            if diet_type == "non_veg":
                dinner = daily_plan.get("dinner")
                if dinner:
                    dinner["portion"] = f"{dinner.get('portion', '')}, optional +50g chicken"
                    dinner["calories"] += 85
                    dinner["protein"] += 15
                    dinner["fat"] += 2
                notes.append("Optional lean-protein bump added for non-veg bulk progression.")

        else:
            notes.append("Maintenance mode: meal balance kept steady for consistent adherence.")

        return notes

    @staticmethod
    def _select_goal_booster(diet_type: str, budget_tier: str) -> Dict[str, Any]:
        booster_priority = {
            "veg": ["curd", "paneer", "milk", "moong_dal"],
            "vegan": ["moong_dal", "chickpea", "peanut_butter"],
            "non_veg": ["egg", "chicken_piece", "curd"],
            "veg_egg": ["egg", "curd", "milk"],
        }
        budget_limit = "affordable" if budget_tier == "affordable" else None
        priorities = booster_priority.get(diet_type, booster_priority["veg"])

        for key in priorities:
            if key not in PROTEIN_BOOSTERS:
                continue
            b = PROTEIN_BOOSTERS[key]
            if diet_type not in b.get("diet_type", []):
                continue
            if budget_limit and IndianDietService._parse_cost_string(b.get("cost", "₹0")) > 25:
                continue
            return b

        return None

    @staticmethod
    def get_diet_tips(goal: str, budget_tier: str, weight: int) -> list:
        """
        Personalized diet tips for Indian users
        """
        tips = {
            "muscle_gain": [
                f"💪 Aim for {int(weight * 2.2)}g protein daily - add eggs, curd, paneer",
                "🍚 Eat rice & dal together - complete amino acid profile",
                "🥚 Have a protein booster (egg/curd) with every meal",
                "📊 Eat 300-400 calories ABOVE your maintenance",
                "⏰ Eat every 3-4 hours to maximize protein synthesis",
                "🥛 Drink milk before sleep for overnight muscle repair",
                "🌶️ Spicy food (chili, turmeric) helps metabolism",
            ],
            "weight_loss": [
                f"🎯 Create 300-500 calorie deficit (eat {int(weight * 20 - 300)}-{int(weight * 20 - 500)} cal/day)",
                "🥬 Load vegetables in your curry - high fiber, low calorie",
                "☕ Skip sugary chai - have black tea or coffee",
                "🚫 Avoid fried items (samosa, pakora) - choose grilled/boiled",
                "💧 Drink water 30 mins before meals - aids digestion",
                "🥚 High protein keeps you full - 35% of calories from protein",
                "⏱️ Slow down eating - 20 mins per meal for satiety",
            ],
            "maintenance": [
                "⚖️ Eat maintenance calories - no surplus or deficit",
                "🎭 Balance all macros - 30% protein, 50% carbs, 20% fat",
                "🌈 Eat colorful vegetables - different nutrients",
                "🍲 Traditional dal-roti is perfectly balanced",
                "📈 Strength train 3-4x/week to maintain muscle",
                "🧘 Include cardio for heart health - walks, running",
                "😴 Sleep 7-8 hours for recovery",
            ],
            "muscle_endurance": [
                f"🔋 Carbs are your friend - 60% of calories from carbs ({int(weight * 3)}g/day)",
                "🍝 Rice, wheat, oats fuel your workouts",
                "🏃 Eat 30-45 mins before workouts - carbs + protein",
                "💪 Moderate protein for endurance (1.8g per kg)",
                "⏰ Timing matters - fuel before and after training",
                "🥤 Stay hydrated - 1L per hour of activity",
                "🧈 Include healthy fats - coconut oil, ghee",
            ]
        }

        budget_specific_tips = {
            "affordable": [
                "🏠 Hostel-friendly: use mess dal/chawal as base and add curd or eggs for protein",
                "🍜 Keep junk to 1-2 meals/week max; pair with protein source to reduce damage",
                "🥚 Cheapest muscle-gain combo: eggs + banana + milk",
                "🛒 Buy staples weekly in bulk: oats, peanuts, rice, dal",
                "🍌 High-value carbs: banana, poha, upma, rice",
                "⚠️ Reality check: ₹100-250/day supports consistency, but high-protein transformation is harder in this slab",
            ],
            "value": [
                "🎯 Budget Hack: Dal-rice is cost-efficient and recovery-friendly",
                "🥚 Buy eggs in bulk - cheapest complete protein option",
                "🛵 Use local tiffin/dhaba meals for better value than apps",
                "🍲 Mix homemade and outside meals to stay consistent",
                "🚀 ₹250-350/day is the practical progress zone for most students",
            ],
            "balanced": [
                "🍲 Add paneer/chicken 3-4 times per week for better protein quality",
                "🏪 Rotate between North and South Indian meals for variety",
                "📱 Plan one high-protein meal daily from outside when busy",
                "🚀 ₹250-350/day is the practical progress zone for most students",
            ],
            "premium": [
                "🥘 Invest in quality protein - paneer, chicken breast",
                "🎁 Try healthy meal services for convenience",
                "🌿 Include organic/premium food items",
                "🥗 Fresh salads for micronutrients",
                "👨‍🍳 Occasional premium meal services",
                "🔥 ₹350-500/day is the optimal transformation zone for physique goals",
            ]
        }

        base_tips = tips.get(goal, [])
        budget_tips = budget_specific_tips.get(budget_tier, [])
        swap_system = [
            "🔁 Swap system: Paneer ↔ Chicken ↔ Eggs ↔ Soya based on budget and diet type",
            "🔁 Carb swap: Roti ↔ Rice ↔ Bread ↔ Oats based on mess availability",
            "🔁 Fat swap: Peanut butter ↔ Peanuts to control cost",
            "🎯 Goal adjuster: fat loss remove 1 carb source, bulk add 1 carb + 1 fat source, maintain keep balanced",
        ]

        return base_tips + budget_tips + swap_system
