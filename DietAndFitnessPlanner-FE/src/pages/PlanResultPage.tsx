import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardActionArea,
  Chip,
  CircularProgress,
  Collapse,
  Container,
  Divider,
  Grid,
  IconButton,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import {
  Bolt,
  ExpandMore,
  FitnessCenter,
  LocalDrink,
  Restaurant,
  TrendingUp,
} from "@mui/icons-material";
import axios from "../api/axiosInstance";
import { useTheme } from "../context/ThemeContext";
import { useNotifications } from "../context/NotificationContext";
import { getTheme } from "../theme/indianTheme";
import ExerciseVideoCard from "../components/ExerciseVideoCard";
import MLRecommendationsPanel from "../components/MLRecommendationsPanel";
import FoodRecognitionPanel from "../components/FoodRecognitionPanel";
import PersonalCoachPanel from "../components/PersonalCoachPanel";

type FormState = {
  name: string;
  email: string;
  age: number;
  heightFeet: number;
  heightInches: number;
  weight: number;
  targetWeight?: number;
  fitnessLevel: string;
  goal: string;
  dietType: string;
  budget_preference: string;
  injury_notes?: string;
  avoid_exercises?: string;
  equipment_access?: string;
  injuryNotes?: string[];
  injuryHistory?: any[];
  avoidExercises?: string[];
  dislikedExercises?: string[];
  equipmentAccess?: string[];
  preferredMuscleGroups?: string[];
  difficultyPreference?: string;
  preferCompound?: boolean;
  performanceHistory?: any[];
};

type MealBreakdown = {
  name: string;
  portion: string;
  macros: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
  };
  cost: string;
  prep_time?: string;
  availability?: string;
  protein_booster?: {
    name: string;
    portion: string;
  };
  explanation?: {
    why_this_meal: string;
    why_now: string;
    goal_alignment: string;
  };
  itemized_costs?: Array<{
    item: string;
    estimated_cost: string;
  }>;
};

type PlanData = {
  status: string;
  user_name: string;
  diet_plan: {
    daily_macros: {
      calories: number;
      protein: number;
      carbs: number;
      fats: number;
    };
    meal_plan: Record<
      string,
      {
        overview: string;
        breakdown: MealBreakdown;
      }
    >;
    diet_tips: string[];
    hydration: string;
    budget_tier: {
      name: string;
      emoji: string;
      description: string;
    };
    bmi: number;
    goal: string;
    experience: string;
    diet_preference: string;
    estimated_daily_cost?: number;
    estimated_daily_cost_range?: {
      min: number;
      max: number;
    };
    spend_strategy?: string;
  };
  fitness_plan: {
    user_info: {
      age: number;
      weight: number;
      fitness_level: string;
      goal: string;
      injury_notes?: string;
      avoid_exercises?: string;
      equipment_access?: string;
    };
    detailed_plan: Record<
      string,
      {
        type: string;
        exercises: Array<{
          name: string;
          sets?: number;
          reps?: string;
          duration?: string;
        }>;
        duration: string;
        recovery_tips: string[];
        warmup?: string[];
        cooldown?: string[];
        precautions?: string[];
        exercise_options?: string[];
      }
    >;
    fitness_tips: string[];
    recovery_recommendations: string[];
    warmup_routine?: string[];
    cooldown_routine?: string[];
    safety_notes?: string[];
    exercise_swaps?: string[];
    injury_context?: {
      injuries?: string[];
      avoid_exercises?: string[];
      replacements?: string[];
      precautions?: string[];
      equipment_access?: string[];
    };
  };
};

const GOAL_LABELS: Record<string, string> = {
  muscle_gain: "Muscle Gain",
  weight_loss: "Fat Loss",
  maintenance: "Maintain Weight",
  muscle_endurance: "Endurance",
};

const DIET_LABELS: Record<string, string> = {
  veg: "Vegetarian",
  non_veg: "Non-Vegetarian",
  vegan: "Vegan",
  eggetarian: "Vegetarian + Eggs",
};

const EXPERIENCE_LABELS: Record<string, string> = {
  amateur: "Amateur",
  intermediate: "Intermediate",
  professional: "Professional",
  beginner: "Beginner",
  advanced: "Advanced",
};

const PlanResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { theme: currentTheme } = useTheme();
  const themeConfig = getTheme(currentTheme);
  const isDark = currentTheme === "dark";
  const { refreshNotifications } = useNotifications();
  const state = (location.state ?? null) as FormState | null;

  const [activeTab, setActiveTab] = useState<"overview" | "diet" | "fitness" | "fitness_videos" | "ml" | "food">("overview");
  const [planData, setPlanData] = useState<PlanData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openMeals, setOpenMeals] = useState<Record<string, boolean>>({});
  const [openWorkouts, setOpenWorkouts] = useState<Record<string, boolean>>({});
  const [exercises, setExercises] = useState<any[]>([]);
  const [exercisesLoading, setExercisesLoading] = useState(false);

  useEffect(() => {
    if (!state) {
      navigate("/details");
      return;
    }

    const fetchPlan = async () => {
      try {
        const response = await axios.post("/generate-plan", state);
        if (response.data.status === "success") {
          setPlanData(response.data as PlanData);
          void refreshNotifications();
        } else {
          setError(response.data.message || "Failed to generate plan");
        }
      } catch (err: unknown) {
        const message =
          (err as { response?: { data?: { message?: string } }; message?: string }).response?.data?.message ||
          (err as { message?: string }).message ||
          "Error fetching plan";
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    void fetchPlan();
  }, [navigate, refreshNotifications, state]);

  useEffect(() => {
    if (activeTab === "fitness_videos" && exercises.length === 0) {
      setExercisesLoading(true);
      axios
        .get("/exercises")
        .then((res) => {
          if (res.data.exercises) {
            setExercises(Object.values(res.data.exercises));
          }
        })
        .catch((err) => console.error("Error loading exercises:", err))
        .finally(() => setExercisesLoading(false));
    }
  }, [activeTab, exercises.length]);

  const dietPlan = planData?.diet_plan;
  const fitnessPlan = planData?.fitness_plan;
  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  const profileChips = useMemo(() => {
    if (!state) return [];
    return [
      `Goal: ${GOAL_LABELS[state.goal] || state.goal}`,
      `Diet: ${DIET_LABELS[state.dietType] || state.dietType}`,
      `Experience: ${EXPERIENCE_LABELS[state.fitnessLevel] || state.fitnessLevel}`,
    ];
  }, [state]);

  const navigationCards = [
    { key: "overview", title: "Overview", description: "Summary, key advice, and plan highlights.", icon: <TrendingUp sx={{ color: accentColor }} /> },
    { key: "diet", title: "Diet Plan", description: "Expandable meal cards with cost and macros.", icon: <Restaurant sx={{ color: accentColor }} /> },
    { key: "fitness", title: "Workout Plan", description: "Weekly training cards with animated details.", icon: <FitnessCenter sx={{ color: accentColor }} /> },
    { key: "fitness_videos", title: "Exercise Videos", description: "Quick access to exercise demos and form tips.", icon: <FitnessCenter sx={{ color: accentColor }} /> },
    { key: "ml", title: "AI Recommendations", description: "Chat with your coach and see ML-backed recommendations.", icon: <Bolt sx={{ color: accentColor }} /> },
    { key: "food", title: "Food Recognition", description: "Scan food and see nutrition analysis.", icon: <LocalDrink sx={{ color: accentColor }} /> },
  ] as const;

  const toggleMeal = (mealKey: string) => {
    setOpenMeals((prev) => ({ ...prev, [mealKey]: !prev[mealKey] }));
  };

  const toggleWorkout = (dayKey: string) => {
    setOpenWorkouts((prev) => ({ ...prev, [dayKey]: !prev[dayKey] }));
  };

  if (!state) return null;

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: isDark
            ? "radial-gradient(circle at 10% 20%, rgba(212,175,55,0.22) 0%, rgba(212,175,55,0) 36%), linear-gradient(125deg, #070707 0%, #101015 58%, #17120f 100%)"
            : "linear-gradient(125deg, #F5F1E8 0%, #FAFAF8 58%, #F8F6F1 100%)",
          transition: "background 0.3s ease",
        }}
      >
        <Box sx={{ textAlign: "center" }}>
          <CircularProgress sx={{ color: isDark ? "#D4AF37" : "#2B5F3A", mb: 2 }} size={56} />
          <Typography sx={{ color: themeConfig.colors.textPrimary }}>Generating your customized plan...</Typography>
        </Box>
      </Box>
    );
  }

  if (error || !planData || !dietPlan || !fitnessPlan) {
    return (
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          p: 2,
          background: isDark
            ? "radial-gradient(circle at 10% 20%, rgba(212,175,55,0.22) 0%, rgba(212,175,55,0) 36%), linear-gradient(125deg, #070707 0%, #101015 58%, #17120f 100%)"
            : "linear-gradient(125deg, #F5F1E8 0%, #FAFAF8 58%, #F8F6F1 100%)",
          transition: "background 0.3s ease",
        }}
      >
        <Paper
          sx={{
            p: 3,
            maxWidth: 680,
            borderRadius: "16px",
            background: isDark ? "rgba(14,14,16,0.84)" : "rgba(255, 255, 255, 0.9)",
            color: themeConfig.colors.textPrimary,
            border: isDark ? "1px solid rgba(212,175,55,0.34)" : "1px solid rgba(43, 95, 58, 0.2)",
          }}
        >
          <Alert severity="error" sx={{ mb: 2 }}>
            {error || "Failed to generate plan."}
          </Alert>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.2}>
            <Button variant="contained" onClick={() => navigate("/details")}>Go Back</Button>
            <Button variant="outlined" onClick={() => window.location.reload()}>Retry</Button>
          </Stack>
        </Paper>
      </Box>
    );
  }

  const heightDisplay = `${state.heightFeet}'${state.heightInches}"`;

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        py: { xs: 2.5, md: 4.2 },
        background: isDark
          ? "radial-gradient(circle at 10% 15%, rgba(212,175,55,0.2) 0%, rgba(212,175,55,0) 36%), linear-gradient(125deg, #070707 0%, #101015 58%, #17120f 100%)"
          : "linear-gradient(125deg, #F5F1E8 0%, #FAFAF8 58%, #F8F6F1 100%)",
        color: themeConfig.colors.textPrimary,
        transition: "background 0.3s ease",
      }}
    >
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Poppins:wght@400;500;600;700&display=swap');`}</style>

      <Container maxWidth="lg">
        <Paper
          sx={{
            borderRadius: "22px",
            background: isDark ? "rgba(14,14,16,0.8)" : "rgba(255, 255, 255, 0.92)",
            border: isDark ? "1px solid rgba(212,175,55,0.36)" : "1px solid rgba(43, 95, 58, 0.2)",
            p: { xs: 2.2, sm: 3, md: 3.6 },
            boxShadow: themeConfig.shadows.medium,
            color: themeConfig.colors.textPrimary,
            backdropFilter: "blur(10px)",
            position: "relative",
            overflow: "hidden",
            "&::before": {
              content: '""',
              position: "absolute",
              inset: 0,
              background: isDark
                ? "linear-gradient(135deg, rgba(212,175,55,0.05), transparent 50%)"
                : "linear-gradient(135deg, rgba(43,95,58,0.06), transparent 50%)",
              pointerEvents: "none",
            },
          }}
        >
          <Typography sx={{ fontFamily: "'Cinzel', serif", fontSize: { xs: "1.9rem", md: "2.6rem" }, color: accentColor, letterSpacing: "0.04em", mb: 0.6 }}>
            Your Result Dashboard
          </Typography>
          <Typography sx={{ color: isDark ? "rgba(248,246,240,0.85)" : "rgba(0, 0, 0, 0.75)", mb: 1.8 }}>
            Customized for {state.name} with your selected goal, diet, budget, and training level.
          </Typography>

          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mb: 2.2 }}>
            {profileChips.map((label) => (
              <Chip
                key={label}
                label={label}
                sx={{
                  color: isDark ? "#f8f6f0" : "#1A1A1A",
                  border: isDark ? "1px solid rgba(212,175,55,0.35)" : "1px solid rgba(43, 95, 58, 0.3)",
                  background: isDark ? "rgba(255,255,255,0.06)" : "rgba(43, 95, 58, 0.08)",
                }}
              />
            ))}
            <Chip
              label={dietPlan.budget_tier.name}
              sx={{
                color: isDark ? "#111" : "#FFFFFF",
                fontWeight: 700,
                background: isDark ? "linear-gradient(135deg, #D4AF37, #E8C969)" : "linear-gradient(135deg, #2B5F3A, #4E9A60)",
              }}
            />
          </Stack>

          <Grid container spacing={1.2} sx={{ mb: 2.2 }}>
            {navigationCards.map((item) => {
              const isActive = activeTab === item.key;

              return (
                <Grid size={{ xs: 12, sm: 6, md: 4 }} key={item.key}>
                  <Card
                    sx={{
                      height: "100%",
                      borderRadius: "16px",
                      background: isActive
                        ? isDark
                          ? "linear-gradient(135deg, rgba(212,175,55,0.15), rgba(255,255,255,0.06))"
                          : "linear-gradient(135deg, rgba(43,95,58,0.12), rgba(255,255,255,0.7))"
                        : isDark
                        ? "rgba(255,255,255,0.05)"
                        : "rgba(0, 0, 0, 0.03)",
                      border: isActive
                        ? `1px solid ${accentColor}`
                        : isDark
                        ? "1px solid rgba(212,175,55,0.18)"
                        : "1px solid rgba(43,95,58,0.14)",
                    }}
                  >
                    <CardActionArea onClick={() => setActiveTab(item.key)} sx={{ height: "100%" }}>
                      <Box sx={{ p: 1.6, display: "flex", gap: 1.2, alignItems: "flex-start" }}>
                        <Box sx={{ width: 42, height: 42, borderRadius: "12px", display: "flex", alignItems: "center", justifyContent: "center", background: isActive ? (isDark ? "rgba(212,175,55,0.16)" : "rgba(43,95,58,0.12)") : isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.04)" }}>
                          {item.icon}
                        </Box>
                        <Box sx={{ minWidth: 0 }}>
                          <Typography sx={{ fontWeight: 700, mb: 0.35 }}>{item.title}</Typography>
                          <Typography sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.75)" : "rgba(0, 0, 0, 0.66)" }}>
                            {item.description}
                          </Typography>
                        </Box>
                      </Box>
                    </CardActionArea>
                  </Card>
                </Grid>
              );
            })}
          </Grid>

          {activeTab === "overview" && (
            <Box>
              <Paper sx={{ p: 2.2, mb: 1.4, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                <Typography sx={{ fontWeight: 700, mb: 1 }}>Your Selection Summary</Typography>
                <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)" }}>
                  {EXPERIENCE_LABELS[state.fitnessLevel] || state.fitnessLevel} level, {GOAL_LABELS[state.goal] || state.goal} goal, {DIET_LABELS[state.dietType] || state.dietType} diet, budget range {dietPlan.budget_tier.name}.
                </Typography>
                <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)", mt: 0.8 }}>
                  Profile: {state.age} yrs, {heightDisplay}, {state.weight} kg.
                </Typography>
              </Paper>

              <Grid container spacing={1.4} sx={{ mb: 1.4 }}>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: "100%", borderRadius: "16px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.22)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                    <CardActionArea onClick={() => setActiveTab("diet")} sx={{ height: "100%" }}>
                      <Box sx={{ p: 1.8 }}>
                        <Stack direction="row" spacing={1.2} alignItems="center" sx={{ mb: 0.8 }}><Restaurant sx={{ color: accentColor }} /><Typography sx={{ fontWeight: 700 }}>Diet Plan</Typography></Stack>
                        <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.72)" }}>
                          {Object.keys(dietPlan.meal_plan).length} meals, {dietPlan.daily_macros.calories} kcal, tap to explore the full breakdown.
                        </Typography>
                      </Box>
                    </CardActionArea>
                  </Card>
                </Grid>

                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: "100%", borderRadius: "16px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.22)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                    <CardActionArea onClick={() => setActiveTab("fitness")} sx={{ height: "100%" }}>
                      <Box sx={{ p: 1.8 }}>
                        <Stack direction="row" spacing={1.2} alignItems="center" sx={{ mb: 0.8 }}><FitnessCenter sx={{ color: accentColor }} /><Typography sx={{ fontWeight: 700 }}>Workout Plan</Typography></Stack>
                        <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.72)" }}>
                          {Object.keys(fitnessPlan.detailed_plan).length} training days with warmups, precautions, and swaps.
                        </Typography>
                      </Box>
                    </CardActionArea>
                  </Card>
                </Grid>

                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: "100%", borderRadius: "16px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.22)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                    <CardActionArea onClick={() => setActiveTab("ml")} sx={{ height: "100%" }}>
                      <Box sx={{ p: 1.8 }}>
                        <Stack direction="row" spacing={1.2} alignItems="center" sx={{ mb: 0.8 }}><Bolt sx={{ color: accentColor }} /><Typography sx={{ fontWeight: 700 }}>AI Recommendations</Typography></Stack>
                        <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.72)" }}>
                          Personalized nutrition and workout guidance generated from your profile.
                        </Typography>
                      </Box>
                    </CardActionArea>
                  </Card>
                </Grid>
              </Grid>

              <Paper sx={{ p: 2.2, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                <Typography sx={{ fontWeight: 700, mb: 1 }}>Key Advice</Typography>
                {dietPlan.diet_tips.slice(0, 6).map((tip, idx) => (
                  <Typography key={idx} sx={{ color: isDark ? "rgba(248,246,240,0.85)" : "rgba(0, 0, 0, 0.8)", mb: 0.5 }}>• {tip}</Typography>
                ))}
              </Paper>
            </Box>
          )}

          {activeTab === "diet" && (
            <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" }, gap: 1.4 }}>
              {Object.entries(dietPlan.meal_plan).map(([mealType, meal]) => {
                const open = !!openMeals[mealType];
                return (
                  <Card key={mealType} sx={{ p: 2, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                      <Box>
                        <Typography sx={{ fontWeight: 700, textTransform: "capitalize" }}>{mealType}</Typography>
                        <Typography sx={{ fontSize: "0.86rem", color: isDark ? "rgba(248,246,240,0.72)" : "rgba(0, 0, 0, 0.62)" }}>
                          {meal.breakdown.name}
                        </Typography>
                      </Box>
                      <Stack direction="row" spacing={0.6} alignItems="center">
                        <Chip size="small" label={`${meal.breakdown.macros.calories} kcal`} sx={{ color: isDark ? "#111" : "#FFFFFF", fontWeight: 700, background: isDark ? "#E8C969" : "linear-gradient(135deg, #2B5F3A, #4E9A60)" }} />
                        <IconButton size="small" onClick={() => toggleMeal(mealType)} aria-label={open ? "Hide meal details" : "Show meal details"} sx={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.25s ease", color: accentColor, border: isDark ? "1px solid rgba(212,175,55,0.22)" : "1px solid rgba(43,95,58,0.18)", background: isDark ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.62)" }}>
                          <ExpandMore />
                        </IconButton>
                      </Stack>
                    </Stack>

                    <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mb: 1.1 }}>
                      <Chip size="small" label={`P ${meal.breakdown.macros.protein}g`} sx={{ color: themeConfig.colors.textPrimary, background: isDark ? "rgba(255,255,255,0.08)" : "rgba(0, 0, 0, 0.05)", border: isDark ? "1px solid rgba(212,175,55,0.2)" : "1px solid rgba(43, 95, 58, 0.2)" }} />
                      <Chip size="small" label={`C ${meal.breakdown.macros.carbs}g`} sx={{ color: themeConfig.colors.textPrimary, background: isDark ? "rgba(255,255,255,0.08)" : "rgba(0, 0, 0, 0.05)", border: isDark ? "1px solid rgba(212,175,55,0.2)" : "1px solid rgba(43, 95, 58, 0.2)" }} />
                      <Chip size="small" label={`F ${meal.breakdown.macros.fat}g`} sx={{ color: themeConfig.colors.textPrimary, background: isDark ? "rgba(255,255,255,0.08)" : "rgba(0, 0, 0, 0.05)", border: isDark ? "1px solid rgba(212,175,55,0.2)" : "1px solid rgba(43, 95, 58, 0.2)" }} />
                    </Stack>

                    <Collapse in={open} timeout={250} unmountOnExit>
                      <Box sx={{ mt: 1 }}>
                        <Divider sx={{ borderColor: isDark ? "rgba(212,175,55,0.24)" : "rgba(43, 95, 58, 0.15)", mb: 1 }} />
                        {meal.breakdown.explanation && (
                          <Box sx={{ mb: 1 }}>
                            <Typography sx={{ fontSize: "0.86rem", color: accentColor, fontWeight: 700 }}>Why This Meal</Typography>
                            <Typography sx={{ fontSize: "0.86rem", color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)", mb: 0.5 }}>{meal.breakdown.explanation.why_this_meal}</Typography>
                            <Typography sx={{ fontSize: "0.86rem", color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)", mb: 0.5 }}>{meal.breakdown.explanation.why_now}</Typography>
                            <Typography sx={{ fontSize: "0.86rem", color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)" }}>{meal.breakdown.explanation.goal_alignment}</Typography>
                          </Box>
                        )}
                        <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.7)" }}>Prep: {meal.breakdown.prep_time || "N/A"}</Typography>
                        <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.7)" }}>Availability: {meal.breakdown.availability || "Common"}</Typography>
                        {!!meal.breakdown.itemized_costs?.length && (
                          <Box sx={{ mt: 0.8 }}>
                            <Typography sx={{ fontSize: "0.85rem", color: accentColor, fontWeight: 700, mb: 0.4 }}>Estimated Item-Wise Cost</Typography>
                            {meal.breakdown.itemized_costs.map((row, idx) => (
                              <Typography key={`${mealType}-cost-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>• {row.item}: {row.estimated_cost}</Typography>
                            ))}
                          </Box>
                        )}
                        {meal.breakdown.protein_booster && (
                          <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.7)", mt: 0.5 }}>
                            Booster: {meal.breakdown.protein_booster.name} ({meal.breakdown.protein_booster.portion})
                          </Typography>
                        )}
                      </Box>
                    </Collapse>
                  </Card>
                );
              })}
            </Box>
          )}

          {activeTab === "fitness" && (
            <Box>
              {(fitnessPlan.warmup_routine?.length || fitnessPlan.cooldown_routine?.length || fitnessPlan.safety_notes?.length) && (
                <Paper sx={{ p: 2, mb: 1.4, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                  <Typography sx={{ fontWeight: 700, mb: 1.1 }}>Injury-Safe Training Guide</Typography>
                  <Typography sx={{ fontSize: "0.9rem", mb: 0.8, color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.72)" }}>
                    {fitnessPlan.user_info.injury_notes?.trim()
                      ? `Focused around: ${fitnessPlan.user_info.injury_notes}`
                      : "The plan includes joint-friendly warmups, cooldowns, and safer exercise substitutions."}
                  </Typography>

                  {!!fitnessPlan.warmup_routine?.length && (
                    <Box sx={{ mb: 1.1 }}>
                      <Typography sx={{ fontWeight: 700, color: accentColor, mb: 0.5 }}>Warmup</Typography>
                      {fitnessPlan.warmup_routine.map((item, idx) => <Typography key={`warmup-${idx}`} sx={{ fontSize: "0.88rem", mb: 0.3 }}>• {item}</Typography>)}
                    </Box>
                  )}

                  {!!fitnessPlan.cooldown_routine?.length && (
                    <Box sx={{ mb: 1.1 }}>
                      <Typography sx={{ fontWeight: 700, color: accentColor, mb: 0.5 }}>Cooldown</Typography>
                      {fitnessPlan.cooldown_routine.map((item, idx) => <Typography key={`cooldown-${idx}`} sx={{ fontSize: "0.88rem", mb: 0.3 }}>• {item}</Typography>)}
                    </Box>
                  )}

                  {!!fitnessPlan.safety_notes?.length && (
                    <Box>
                      <Typography sx={{ fontWeight: 700, color: accentColor, mb: 0.5 }}>Precautions</Typography>
                      {fitnessPlan.safety_notes.slice(0, 5).map((item, idx) => <Typography key={`precaution-${idx}`} sx={{ fontSize: "0.88rem", mb: 0.3 }}>• {item}</Typography>)}
                    </Box>
                  )}
                </Paper>
              )}

              <Stack spacing={1.2}>
                {Object.entries(fitnessPlan.detailed_plan).map(([day, workout]) => {
                  const open = !!openWorkouts[day];
                  return (
                    <Card key={day} sx={{ p: 2, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                        <Box>
                          <Typography sx={{ fontWeight: 700 }}>{day}</Typography>
                          <Typography sx={{ fontSize: "0.86rem", color: isDark ? "rgba(248,246,240,0.72)" : "rgba(0, 0, 0, 0.62)" }}>{workout.type}</Typography>
                        </Box>
                        <Stack direction="row" spacing={0.6} alignItems="center">
                          <Chip label={workout.duration} size="small" sx={{ color: isDark ? "#111" : "#FFFFFF", background: isDark ? "#E8C969" : "linear-gradient(135deg, #2B5F3A, #4E9A60)" }} />
                          <IconButton size="small" onClick={() => toggleWorkout(day)} aria-label={open ? `Hide ${day} details` : `Show ${day} details`} sx={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.25s ease", color: accentColor, border: isDark ? "1px solid rgba(212,175,55,0.22)" : "1px solid rgba(43,95,58,0.18)", background: isDark ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.62)" }}>
                            <ExpandMore />
                          </IconButton>
                        </Stack>
                      </Stack>

                      <Collapse in={open} timeout={250} unmountOnExit>
                        <Box>
                          <Stack spacing={0.5}>
                            {workout.exercises.slice(0, 5).map((ex, idx) => (
                              <Typography key={`${day}-${idx}`} sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.7)" }}>
                                • {ex.name}
                                {ex.sets ? ` (${ex.sets} sets)` : ""}
                                {ex.reps ? ` x ${ex.reps}` : ""}
                                {ex.duration ? `, ${ex.duration}` : ""}
                              </Typography>
                            ))}
                          </Stack>
                          {!!workout.precautions?.length && (
                            <Box sx={{ mt: 1 }}>
                              <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>Day Precautions</Typography>
                              {workout.precautions.slice(0, 3).map((item, idx) => <Typography key={`${day}-precaution-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>• {item}</Typography>)}
                            </Box>
                          )}
                          {!!workout.exercise_options?.length && (
                            <Box sx={{ mt: 1 }}>
                              <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>Safer Options</Typography>
                              <Typography sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>
                                {workout.exercise_options.slice(0, 4).join(" • ")}
                              </Typography>
                            </Box>
                          )}
                        </Box>
                      </Collapse>
                    </Card>
                  );
                })}
              </Stack>

              <Paper sx={{ mt: 1.4, p: 2, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                <Typography sx={{ fontWeight: 700, mb: 1.2 }}>Recovery & Tips</Typography>
                {fitnessPlan.recovery_recommendations.slice(0, 4).map((tip, idx) => (
                  <Typography key={idx} sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)", mb: 0.45 }}>• {tip}</Typography>
                ))}
              </Paper>

              {!!dietPlan.spend_strategy && (
                <Paper sx={{ mt: 1.4, p: 2, borderRadius: "14px", background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)", border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
                  <Typography sx={{ fontWeight: 700, mb: 0.8 }}>Budget Clarity</Typography>
                  <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0, 0, 0, 0.75)" }}>{dietPlan.spend_strategy}</Typography>
                </Paper>
              )}
            </Box>
          )}

          {activeTab === "fitness_videos" && (
            <Box>
              <Typography sx={{ fontWeight: 700, fontSize: "1.1rem", mb: 1.4 }}>💪 Exercise Library with Form Tips</Typography>
              {exercisesLoading ? (
                <Box sx={{ display: "flex", justifyContent: "center", p: 3 }}><CircularProgress sx={{ color: accentColor }} /></Box>
              ) : (
                <Grid container spacing={1.5}>
                  {exercises.map((exercise: any) => (
                    <Grid size={{ xs: 12, md: 6 }} key={exercise.id}><ExerciseVideoCard exercise={exercise} isDark={isDark} email={state.email || ""} /></Grid>
                  ))}
                </Grid>
              )}
            </Box>
          )}

          {activeTab === "ml" && (
            <Stack spacing={1.8}>
              <Paper
                sx={{
                  p: 2.2,
                  borderRadius: "16px",
                  background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0, 0, 0, 0.03)",
                  border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
                }}
              >
                <Typography sx={{ fontWeight: 800, fontSize: "1.05rem", color: accentColor, mb: 0.6 }}>
                  Ask your AI coach first
                </Typography>
                <Typography sx={{ color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0,0,0,0.72)" }}>
                  Use chat for meal swaps, calorie guidance, workout questions, and recovery help. The ML insights stay below it.
                </Typography>
              </Paper>

              <PersonalCoachPanel
                email={state.email || ""}
                currentPlan={planData}
                userProfile={{
                  name: state.name,
                  email: state.email,
                  age: state.age,
                  heightFeet: state.heightFeet,
                  heightInches: state.heightInches,
                  weight: state.weight,
                  target_weight: state.targetWeight,
                  fitnessLevel: state.fitnessLevel,
                  goal: state.goal,
                  dietType: state.dietType,
                  budget_preference: state.budget_preference,
                  injury_notes: state.injuryNotes || [],
                  injury_history: state.injuryHistory || [],
                  avoid_exercises: state.avoidExercises || [],
                  disliked_exercises: state.dislikedExercises || [],
                  equipment_access: state.equipmentAccess || [],
                  preferred_muscle_groups: state.preferredMuscleGroups || [],
                  difficulty_preference: state.difficultyPreference || state.fitnessLevel || "intermediate",
                  prefer_compound: Boolean(state.preferCompound),
                  performance_history: state.performanceHistory || [],
                }}
                isDark={isDark}
              />

              <Divider sx={{ borderColor: isDark ? "rgba(212,175,55,0.2)" : "rgba(43, 95, 58, 0.12)" }} />

              <MLRecommendationsPanel
                email={state.email || ""}
                userProfile={{
                  weight: state.weight || 70,
                  target_weight: state.targetWeight,
                  age: state.age || 25,
                  fitness_level: state.fitnessLevel || "intermediate",
                  goal: state.goal || "maintenance",
                  injury_notes: state.injuryNotes || [],
                  injury_history: state.injuryHistory || [],
                  avoid_exercises: state.avoidExercises || [],
                  disliked_exercises: state.dislikedExercises || [],
                  equipment_access: state.equipmentAccess || [],
                  preferred_muscle_groups: state.preferredMuscleGroups || [],
                  difficulty_preference: state.difficultyPreference || state.fitnessLevel || "intermediate",
                  prefer_compound: Boolean(state.preferCompound),
                  performance_history: state.performanceHistory || [],
                }}
                isDark={isDark}
              />
            </Stack>
          )}

          {activeTab === "food" && <FoodRecognitionPanel isDark={isDark} />}

          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.2} sx={{ mt: 2.3 }}>
            <Button
              variant="contained"
              startIcon={<Restaurant />}
              onClick={() => navigate("/details")}
              sx={{
                textTransform: "none",
                borderRadius: "999px",
                bgcolor: accentColor,
                color: isDark ? "#121212" : "#FFFFFF",
                fontWeight: 700,
                "&:hover": { bgcolor: isDark ? "#E8C969" : "#214C2E" },
              }}
            >
              Regenerate Plan
            </Button>
            <Button
              variant="outlined"
              startIcon={<FitnessCenter />}
              onClick={() => navigate("/login")}
              sx={{
                textTransform: "none",
                borderRadius: "999px",
                borderColor: isDark ? "rgba(255,255,255,0.45)" : "rgba(0, 0, 0, 0.2)",
                color: themeConfig.colors.textPrimary,
                "&:hover": {
                  borderColor: accentColor,
                  backgroundColor: isDark ? "rgba(212, 175, 55, 0.08)" : "rgba(43, 95, 58, 0.08)",
                },
              }}
            >
              Back to Login
            </Button>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
};

export default PlanResultPage;
