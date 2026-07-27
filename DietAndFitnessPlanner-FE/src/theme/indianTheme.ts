import type { ThemeMode } from "../context/ThemeContext";

// === DARK THEME (Gold & Black) ===
export const DarkTheme = {
  colors: {
    primary: "#FF6B35", // Saffron - energetic, bold
    secondary: "#004E89", // Deep Blue - trust, strength
    accent: "#00BA63", // Green - health, growth
    warning: "#FFA500", // Orange
    danger: "#E74C3C",

    // Backgrounds
    bgLight: "#FFF9F0", // Cream - warm, inviting
    bgDark: "#0b0b0c", // Near black
    bgCard: "#161212", // Card background

    // Text colors
    textPrimary: "#f8f6f0", // Light text
    textSecondary: "#b0a890",
    textLight: "#FFFFFF",

    // Accent colors
    gold: "#FFD700",
    copper: "#B87333",
    saffron: "#FF6B35",
    indianGreen: "#00BA63",
  },

  typography: {
    fontFamily: "'Poppins', 'Inter', sans-serif",
    heroFont: "'Outfit', 'Poppins', sans-serif",
  },

  gradients: {
    primary: "linear-gradient(135deg, #FF6B35 0%, #FFA500 100%)",
    secondary: "linear-gradient(135deg, #004E89 0%, #0A7FBB 100%)",
    success: "linear-gradient(135deg, #00BA63 0%, #00D4AA 100%)",
    sunSet: "linear-gradient(135deg, #FF6B35 0%, #FFA500 50%, #FFD700 100%)",
    ocean: "linear-gradient(135deg, #004E89 0%, #0A7FBB 50%, #00BA63 100%)",
  },

  shadows: {
    light: "0 2px 8px rgba(0, 0, 0, 0.3)",
    medium: "0 4px 16px rgba(0, 0, 0, 0.4)",
    heavy: "0 8px 32px rgba(0, 0, 0, 0.5)",
    indianGlow: "0 4px 20px rgba(255, 107, 53, 0.4)",
  },

  borderRadius: {
    small: "8px",
    medium: "12px",
    large: "16px",
    xl: "20px",
  },
};

// === LIGHT THEME (Fresh & Green) ===
export const LightTheme = {
  colors: {
    primary: "#2B5F3A", // Primary green for light mode
    secondary: "#004E89", // Deep Blue - trust, strength
    accent: "#00BA63", // Green - health, growth
    warning: "#4E9A60", // Soft green warning accent
    danger: "#E74C3C",

    // Backgrounds
    bgLight: "#F8F5F0", // Warm cream background
    bgDark: "#FFFFFF", // White background
    bgCard: "#FCFBF9", // Card background - warm off-white

    // Text colors
    textPrimary: "#2D2D2D", // Dark text with slight warmth
    textSecondary: "#5A5A5A",
    textLight: "#FFFFFF",

    // Accent colors
    gold: "#FFD700",
    copper: "#B87333",
    saffron: "#2B5F3A",
    indianGreen: "#00BA63",
  },

  typography: {
    fontFamily: "'Poppins', 'Inter', sans-serif",
    heroFont: "'Outfit', 'Poppins', sans-serif",
  },

  gradients: {
    primary: "linear-gradient(135deg, #2B5F3A 0%, #4E9A60 100%)",
    secondary: "linear-gradient(135deg, #004E89 0%, #0A7FBB 100%)",
    success: "linear-gradient(135deg, #00BA63 0%, #00D4AA 100%)",
    sunSet: "linear-gradient(135deg, #2B5F3A 0%, #4E9A60 50%, #7FBE8C 100%)",
    ocean: "linear-gradient(135deg, #004E89 0%, #0A7FBB 50%, #00BA63 100%)",
  },

  shadows: {
    light: "0 2px 8px rgba(0, 0, 0, 0.08)",
    medium: "0 4px 16px rgba(0, 0, 0, 0.1)",
    heavy: "0 8px 32px rgba(0, 0, 0, 0.12)",
    indianGlow: "0 4px 20px rgba(0, 186, 99, 0.15)",
  },

  borderRadius: {
    small: "8px",
    medium: "12px",
    large: "16px",
    xl: "20px",
  },
};

// Function to get current theme based on mode
export const getTheme = (mode: ThemeMode) => {
  return mode === "dark" ? DarkTheme : LightTheme;
};

// Export for backward compatibility
export const IndianTheme = DarkTheme;

// English text with Indian theme
export const AppText = {
  common: {
    welcome: "Welcome! 🙏",
    login: "Login",
    register: "Sign Up",
    logout: "Logout",
    next: "Next →",
    back: "Back ←",
    submit: "Submit",
    cancel: "Cancel",
  },

  landing: {
    hero: "Fitness for Indian College & Hostel Students",
    tagline: "Your Budget, Your Body, Your Goals",
    cta: "Get Started →",
    quote: "Fitness is not a destination, it's a lifestyle.",
  },

  login: {
    title: "Login to Your Dream Body",
    placeholder: {
      email: "Your Email",
      password: "Password (Keep it strong!)",
    },
  },

  userDetails: {
    title: "Tell us about yourself 💪",
    subtitle: "So we can create the perfect plan for you",
    fields: {
      name: "Full Name",
      email: "Email",
      age: "Age",
      height: "Height (Feet-Inches)",
      weight: "Weight (in kg)",
      fitnessLevel: "Fitness Level",
      goal: "Your Goal",
      dietType: "Diet Preference",
      budget: "Monthly Budget for Food",
    },
    options: {
      fitnessLevel: ["Beginner", "Intermediate", "Active", "Very Active"],
      goal: ["Build Muscle", "Lose Weight", "Stay Fit", "Build Endurance"],
      dietType: ["Vegetarian", "Non-Vegetarian", "Both"],
      budget: ["Budget (₹300-400/day)", "Moderate (₹400-600/day)", "Premium (₹600+/day)"],
    },
  },

  result: {
    title: "Your Personal Plan is Ready! 🎉",
    dailyPlan: "Your Daily Meal Plan",
    breakfastTime: "Breakfast - 7-8 AM",
    lunchTime: "Lunch - 1-2 PM",
    snackTime: "Snacks - 4-5 PM",
    dinnerTime: "Dinner - 8-9 PM",
    dailyTargets: "Your Daily Targets",
    protein: "Protein",
    carbs: "Carbohydrates",
    fat: "Fat",
    calories: "Calories",
    tips: "Tips for You",
  },

  units: {
    calories: "Calories",
    grams: "g",
    cost: "Cost",
    prepTime: "Prep Time",
    availability: "Availability",
  },

  messages: {
    success: "Success! Your plan is ready",
    error: "Something went wrong. Please try again",
    loading: "Creating your plan...",
    backendError: "Server connection failed. Please try again later.",
  },
};

// Budget tier descriptions
export const BudgetDescriptions = {
  budget: {
    emoji: "🎒",
    name: "Hostel Student",
    desc: "₹300-400/day budget",
    meals: ["Poha", "Maggi", "Dal-Rice", "Roti-Sabzi"],
    color: "#2B5F3A",
  },
  moderate: {
    emoji: "💼",
    name: "Working Professional",
    desc: "₹400-600/day budget",
    meals: ["Chicken", "Paneer", "Biryani", "Dal Makhani"],
    color: "#004E89",
  },
  premium: {
    emoji: "⭐",
    name: "Premium Budget",
    desc: "₹600+/day budget",
    meals: ["Protein Shake", "Gym Mess", "Premium Chicken"],
    color: "#00BA63",
  },
};

export const GoalEmojis = {
  muscle_gain: "💪",
  weight_loss: "🏃",
  maintenance: "⚖️",
  muscle_endurance: "🔋",
};

export const FitnessLevelEmojis = {
  sedentary: "🪑",
  light: "🚶",
  moderate: "🚴",
  active: "🏃",
  very_active: "🤸",
};

