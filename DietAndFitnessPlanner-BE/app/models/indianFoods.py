# Indian Food Database with Macronutrients (per 100g unless specified)
# Designed for budget-conscious college students, hostel dwellers, and working professionals

INDIAN_BREAKFAST_OPTIONS = {
    # Budget-friendly options under ₹30-50
    "poha": {
        "name": "Poha (with peanuts)",
        "portion": "1 plate (150g)",
        "calories": 220,
        "protein": 6,
        "carbs": 42,
        "fat": 3,
        "cost": "₹20-30",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "maggi": {
        "name": "Maggi Noodles",
        "portion": "1 pack (80g)",
        "calories": 380,
        "protein": 10,
        "carbs": 55,
        "fat": 12,
        "cost": "₹15-20",
        "prep_time": "3 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "chai_biscuit": {
        "name": "Chai + 2 Biscuits",
        "portion": "1 cup chai + 2 biscuits",
        "calories": 180,
        "protein": 3,
        "carbs": 32,
        "fat": 5,
        "cost": "₹15-25",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "dosa": {
        "name": "Dosa (plain)",
        "portion": "1 dosa (150g)",
        "calories": 280,
        "protein": 8,
        "carbs": 50,
        "fat": 4,
        "cost": "₹30-50",
        "prep_time": "10 mins",
        "availability": "Most places",
        "diet_type": ["veg", "vegan"]
    },
    "idli_sambar": {
        "name": "Idli (2) + Sambar",
        "portion": "2 idlis (100g) + sambar",
        "calories": 180,
        "protein": 6,
        "carbs": 35,
        "fat": 2,
        "cost": "₹30-40",
        "prep_time": "10 mins",
        "availability": "South Indian areas",
        "diet_type": ["veg", "vegan"]
    },
    "upma": {
        "name": "Upma (plain)",
        "portion": "1 bowl (150g)",
        "calories": 240,
        "protein": 7,
        "carbs": 38,
        "fat": 6,
        "cost": "₹20-30",
        "prep_time": "10 mins",
        "availability": "Most places",
        "diet_type": ["veg", "vegan"]
    },
    "bread_butter": {
        "name": "Bread (2 slices) + Butter",
        "portion": "2 slices + 1 tbsp butter",
        "calories": 220,
        "protein": 6,
        "carbs": 24,
        "fat": 10,
        "cost": "₹15-20",
        "prep_time": "2 mins",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "bread_egg": {
        "name": "Bread (2) + Fried Egg",
        "portion": "2 slices + 1 egg",
        "calories": 280,
        "protein": 12,
        "carbs": 24,
        "fat": 14,
        "cost": "₹25-35",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg_egg", "non_veg"]
    },
    "oats_milk": {
        "name": "Oats + Milk",
        "portion": "40g oats + 200ml milk",
        "calories": 260,
        "protein": 11,
        "carbs": 38,
        "fat": 6,
        "cost": "₹30-40",
        "prep_time": "5 mins",
        "availability": "Most grocery stores",
        "diet_type": ["veg"]
    },
    "banana": {
        "name": "Banana (2-3)",
        "portion": "250g",
        "calories": 220,
        "protein": 3,
        "carbs": 56,
        "fat": 0.5,
        "cost": "₹20-30",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
}

INDIAN_LUNCH_OPTIONS = {
    # Main meal options
    "dal_rice": {
        "name": "Dal (Arhar) + Rice",
        "portion": "150g dal + 150g rice",
        "calories": 420,
        "protein": 14,
        "carbs": 72,
        "fat": 4,
        "cost": "₹30-40",
        "prep_time": "30 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "roti_sabzi": {
        "name": "Roti (3) + Mixed Vegetable Curry",
        "portion": "3 rotis + 150g curry",
        "calories": 380,
        "protein": 12,
        "carbs": 65,
        "fat": 8,
        "cost": "₹35-45",
        "prep_time": "30 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "roti_dhal": {
        "name": "Roti (3) + Dal (Tadka)",
        "portion": "3 rotis + 150g dal",
        "calories": 440,
        "protein": 16,
        "carbs": 68,
        "fat": 10,
        "cost": "₹30-40",
        "prep_time": "30 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "rice_sabzi": {
        "name": "Rice (200g) + Vegetable Curry",
        "portion": "200g rice + 150g curry",
        "calories": 420,
        "protein": 10,
        "carbs": 78,
        "fat": 6,
        "cost": "₹30-40",
        "prep_time": "25 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "biryani": {
        "name": "Chicken Biryani",
        "portion": "300g",
        "calories": 520,
        "protein": 22,
        "carbs": 62,
        "fat": 18,
        "cost": "₹80-120",
        "prep_time": "45 mins",
        "availability": "Restaurant",
        "diet_type": ["non_veg"]
    },
    "dal_makhani": {
        "name": "Dal Makhani + Roti (3)",
        "portion": "150g dal + 3 rotis",
        "calories": 480,
        "protein": 14,
        "carbs": 64,
        "fat": 16,
        "cost": "₹40-50",
        "prep_time": "45 mins",
        "availability": "Home/Restaurant",
        "diet_type": ["veg"]
    },
    "chole_puri": {
        "name": "Chole (Chickpea Curry) + Puri (2)",
        "portion": "150g chole + 2 puris",
        "calories": 480,
        "protein": 12,
        "carbs": 64,
        "fat": 16,
        "cost": "₹35-45",
        "prep_time": "40 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "rajma_rice": {
        "name": "Rajma (Kidney Beans) + Rice",
        "portion": "150g rajma + 150g rice",
        "calories": 420,
        "protein": 16,
        "carbs": 72,
        "fat": 4,
        "cost": "₹30-40",
        "prep_time": "30 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "fish_curry": {
        "name": "Fish Curry + Rice",
        "portion": "150g fish + 150g rice",
        "calories": 380,
        "protein": 28,
        "carbs": 55,
        "fat": 8,
        "cost": "₹90-120",
        "prep_time": "40 mins",
        "availability": "Coastal areas",
        "diet_type": ["non_veg"]
    },
    "mutton_curry": {
        "name": "Mutton Curry + Roti (3)",
        "portion": "150g mutton + 3 rotis",
        "calories": 520,
        "protein": 32,
        "carbs": 65,
        "fat": 18,
        "cost": "₹120-150",
        "prep_time": "60 mins",
        "availability": "Most places",
        "diet_type": ["non_veg"]
    },
    "paneer_sabzi": {
        "name": "Paneer Curry (Butter Paneer) + Roti (2)",
        "portion": "100g paneer + 2 rotis",
        "calories": 420,
        "protein": 18,
        "carbs": 48,
        "fat": 16,
        "cost": "₹60-80",
        "prep_time": "25 mins",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "chicken_curry": {
        "name": "Chicken Curry + Rice/Roti",
        "portion": "150g chicken + 150g rice",
        "calories": 450,
        "protein": 28,
        "carbs": 55,
        "fat": 12,
        "cost": "₹80-100",
        "prep_time": "40 mins",
        "availability": "Most places",
        "diet_type": ["non_veg"]
    },
}

INDIAN_SNACKS_OPTIONS = {
    # Between meal options (optional)
    "chai_samosa": {
        "name": "Chai + Samosa",
        "portion": "1 cup + 1 samosa",
        "calories": 280,
        "protein": 5,
        "carbs": 42,
        "fat": 10,
        "cost": "₹30-40",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "banana_chips": {
        "name": "Banana Chips",
        "portion": "50g",
        "calories": 240,
        "protein": 2,
        "carbs": 28,
        "fat": 14,
        "cost": "₹15-20",
        "prep_time": "1 min",
        "availability": "Most shops",
        "diet_type": ["veg", "vegan"]
    },
    "peanuts": {
        "name": "Roasted Peanuts",
        "portion": "50g",
        "calories": 280,
        "protein": 10,
        "carbs": 10,
        "fat": 24,
        "cost": "₹20-30",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "namkeen": {
        "name": "Namkeen (Salty Snack)",
        "portion": "50g",
        "calories": 260,
        "protein": 5,
        "carbs": 28,
        "fat": 14,
        "cost": "₹15-25",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "biscuit_tea": {
        "name": "Biscuit + Tea",
        "portion": "2 biscuits + tea",
        "calories": 180,
        "protein": 3,
        "carbs": 30,
        "fat": 6,
        "cost": "₹15-20",
        "prep_time": "3 mins",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "curd": {
        "name": "Curd (Plain)",
        "portion": "200g",
        "calories": 120,
        "protein": 11,
        "carbs": 6,
        "fat": 4,
        "cost": "₹15-25",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "buttermilk": {
        "name": "Buttermilk (Chaach)",
        "portion": "250ml",
        "calories": 100,
        "protein": 8,
        "carbs": 8,
        "fat": 2,
        "cost": "₹10-15",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
    "fruit": {
        "name": "Apple/Orange",
        "portion": "200g",
        "calories": 100,
        "protein": 0.5,
        "carbs": 25,
        "fat": 0.3,
        "cost": "₹20-30",
        "prep_time": "1 min",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "egg_snack": {
        "name": "Boiled Eggs (2) + Toast",
        "portion": "2 eggs + 1 slice",
        "calories": 240,
        "protein": 18,
        "carbs": 12,
        "fat": 12,
        "cost": "₹20-30",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg_egg", "non_veg"]
    },
    "chicken_snack": {
        "name": "Grilled Chicken Snack",
        "portion": "100g",
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6,
        "cost": "₹50-70",
        "prep_time": "10 mins",
        "availability": "Most shops",
        "diet_type": ["non_veg"]
    },
    "paneer_snack": {
        "name": "Paneer Cheese Bites",
        "portion": "100g",
        "calories": 180,
        "protein": 20,
        "carbs": 2,
        "fat": 10,
        "cost": "₹40-60",
        "prep_time": "5 mins",
        "availability": "Everywhere",
        "diet_type": ["veg"]
    },
}

INDIAN_DINNER_OPTIONS = {
    # Similar to lunch but lighter options
    "dal_rice_light": {
        "name": "Dal (Light) + Rice",
        "portion": "100g dal + 100g rice",
        "calories": 280,
        "protein": 10,
        "carbs": 50,
        "fat": 2,
        "cost": "₹25-35",
        "prep_time": "25 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "roti_sabzi_light": {
        "name": "Roti (2) + Light Vegetable Curry",
        "portion": "2 rotis + 100g curry",
        "calories": 260,
        "protein": 9,
        "carbs": 46,
        "fat": 5,
        "cost": "₹25-35",
        "prep_time": "25 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "soup_bread": {
        "name": "Vegetable Soup + Bread (2)",
        "portion": "250ml soup + 2 slices",
        "calories": 200,
        "protein": 6,
        "carbs": 38,
        "fat": 3,
        "cost": "₹20-30",
        "prep_time": "20 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "khichdi": {
        "name": "Khichdi (Dal + Rice + Ghee)",
        "portion": "300g",
        "calories": 360,
        "protein": 12,
        "carbs": 58,
        "fat": 8,
        "cost": "₹30-40",
        "prep_time": "20 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "moong_dal_light": {
        "name": "Moong Dal (Light) + Roti (2)",
        "portion": "100g dal + 2 rotis",
        "calories": 280,
        "protein": 12,
        "carbs": 50,
        "fat": 3,
        "cost": "₹25-35",
        "prep_time": "20 mins",
        "availability": "Everywhere",
        "diet_type": ["veg", "vegan"]
    },
    "egg_curry": {
        "name": "Egg Curry + Roti (2)",
        "portion": "2 eggs + 2 rotis",
        "calories": 320,
        "protein": 16,
        "carbs": 38,
        "fat": 12,
        "cost": "₹30-40",
        "prep_time": "20 mins",
        "availability": "Everywhere",
        "diet_type": ["veg_egg", "non_veg"]
    },
    "curd_rice": {
        "name": "Curd Rice",
        "portion": "300g",
        "calories": 240,
        "protein": 12,
        "carbs": 42,
        "fat": 4,
        "cost": "₹30-40",
        "prep_time": "10 mins",
        "availability": "Most places",
        "diet_type": ["veg"]
    },
    "egg_dinner": {
        "name": "Egg Curry + Roti (2)",
        "portion": "3 eggs + 2 rotis",
        "calories": 340,
        "protein": 20,
        "carbs": 38,
        "fat": 14,
        "cost": "₹35-50",
        "prep_time": "20 mins",
        "availability": "Everywhere",
        "diet_type": ["veg_egg", "non_veg"]
    },
    "chicken_light": {
        "name": "Grilled Chicken + Salad",
        "portion": "150g chicken + 150g salad",
        "calories": 250,
        "protein": 35,
        "carbs": 8,
        "fat": 8,
        "cost": "₹80-100",
        "prep_time": "15 mins",
        "availability": "Most places",
        "diet_type": ["non_veg"]
    },
}

# Protein-boosting add-ons to meet fitness goals
PROTEIN_BOOSTERS = {
    "egg": {
        "name": "1 Boiled Egg",
        "portion": "1 egg (50g)",
        "calories": 78,
        "protein": 6,
        "carbs": 0.6,
        "fat": 5.3,
        "cost": "₹5-8",
        "diet_type": ["veg_egg", "non_veg"]
    },
    "chicken_piece": {
        "name": "Grilled Chicken",
        "portion": "100g",
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6,
        "cost": "₹40-60",
        "diet_type": ["non_veg"]
    },
    "paneer": {
        "name": "Paneer (Cottage Cheese)",
        "portion": "100g",
        "calories": 265,
        "protein": 26,
        "carbs": 1.2,
        "fat": 17,
        "cost": "₹60-80",
        "diet_type": ["veg"]
    },
    "curd": {
        "name": "Greek/Full Fat Curd",
        "portion": "150g",
        "calories": 180,
        "protein": 16,
        "carbs": 9,
        "fat": 7,
        "cost": "₹20-30",
        "diet_type": ["veg"]
    },
    "moong_dal": {
        "name": "Cooked Moong Dal",
        "portion": "100g",
        "calories": 95,
        "protein": 7,
        "carbs": 16,
        "fat": 0.4,
        "cost": "₹15-20",
        "diet_type": ["veg", "vegan"]
    },
    "chickpea": {
        "name": "Cooked Chickpea/Chole",
        "portion": "100g",
        "calories": 134,
        "protein": 8,
        "carbs": 22,
        "fat": 2,
        "cost": "₹15-20",
        "diet_type": ["veg", "vegan"]
    },
    "milk": {
        "name": "Whole Milk",
        "portion": "250ml",
        "calories": 160,
        "protein": 8,
        "carbs": 12,
        "fat": 8,
        "cost": "₹20-25",
        "diet_type": ["veg"]
    },
    "peanut_butter": {
        "name": "Peanut Butter",
        "portion": "2 tbsp (32g)",
        "calories": 188,
        "protein": 8,
        "carbs": 6,
        "fat": 16,
        "cost": "₹15-20",
        "diet_type": ["veg", "vegan"]
    },
}

# Budget-tier definitions
BUDGET_TIERS = {
    "affordable": {
        "name": "Super Affordable (₹100-250/day)",
        "emoji": "🧺",
        "description": "Most economical meals with high value",
        "color": "#F59E0B",
        "meal_cost": "₹20-45",
        "foods": ["poha", "upma", "chai_biscuit", "bread_butter", "dal_rice", "roti_sabzi", "idli_sambar", "bread_egg", "egg_snack"]
    },
    "value": {
        "name": "Best Zone (₹250-350/day)",
        "emoji": "🎒",
        "description": "Practical progress range for most users",
        "color": "#FB7185",
        "meal_cost": "₹35-60",
        "foods": ["poha", "maggi", "chai_biscuit", "dal_rice", "roti_sabzi", "upma", "bread_butter", "idli_sambar", "rice_sabzi", "roti_dhal", "bread_egg", "egg_snack"]
    },
    "balanced": {
        "name": "Best Zone Plus (₹250-350/day)",
        "emoji": "💼",
        "description": "Higher variety but still inside the practical progress range",
        "color": "#22D3EE",
        "meal_cost": "₹50-85",
        "foods": ["dosa", "paneer_sabzi", "dal_makhani", "roti_dhal", "rice_sabzi", "chole_puri", "rajma_rice", "biryani"]
    },
    "premium": {
        "name": "Optimal (₹350-500/day)",
        "emoji": "⭐",
        "description": "Best transformation range with stronger protein coverage",
        "color": "#95E1D3",
        "meal_cost": "₹75-120",
        "foods": ["chicken_curry", "paneer_sabzi", "biryani", "dal_makhani", "chole_puri", "rajma_rice", "rice_sabzi"]
    }
}
