import { useEffect, useState } from "react";
import {
  Card,
  Typography,
  Box,
  Stack,
  CircularProgress,
  Alert,
  Chip,
  Paper,
  LinearProgress,
  Grid,
} from "@mui/material";
import {
  TrendingUp as TrendingUpIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
} from "@mui/icons-material";
import axios from "../api/axiosInstance";

type UserProfile = {
  weight: number;
  age: number;
  target_weight?: number;
  fitness_level: string;
  goal: string;
  injury_notes?: string[];
  injury_history?: Array<Record<string, unknown>>;
  avoid_exercises?: string[];
  disliked_exercises?: string[];
  equipment_access?: string[];
  preferred_muscle_groups?: string[];
  difficulty_preference?: string;
  prefer_compound?: boolean;
  performance_history?: Array<Record<string, unknown>>;
};

type RecommendationSection = Record<string, unknown>;

type ExerciseRecommendation = Record<string, unknown>;

type SwapRecommendation = Record<string, unknown>;

interface MLRecommendationsPanelProps {
  email: string;
  userProfile: UserProfile;
  isDark: boolean;
}

interface Recommendations {
  nutrition: RecommendationSection;
  meal_timing: RecommendationSection;
  exercise_personalization: RecommendationSection;
  goal_achievement: RecommendationSection;
  workout_blueprint?: RecommendationSection;
}

const MLRecommendationsPanel = ({
  email,
  userProfile,
  isDark,
}: MLRecommendationsPanelProps) => {
  const [recommendations, setRecommendations] = useState<Recommendations | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    nutrition: true,
    personalization: true,
    goals: false,
  });

  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await axios.post(
          `/ml/comprehensive-recommendations/${email}`,
          userProfile
        );
        if (response.data.status === "success") {
          setRecommendations(response.data.recommendations);
        } else {
          setError("Failed to fetch recommendations");
        }
      } catch (err) {
        console.error("Error fetching recommendations:", err);
        setError("Error loading ML recommendations");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [email, userProfile]);

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", p: 3 }}>
        <CircularProgress sx={{ color: accentColor }} />
      </Box>
    );
  }

  if (error || !recommendations) {
    return (
      <Alert severity="info" sx={{ borderRadius: "10px" }}>
        {error || "Recommendations not available"}
      </Alert>
    );
  }

  const nutrition = recommendations.nutrition;
  const dailyCalories = nutrition?.daily_calories ?? nutrition?.calories ?? 0;
  const goalData = recommendations.goal_achievement;
  const exerciseBlueprint = recommendations.exercise_personalization || recommendations.workout_blueprint;
  const exercises = Array.isArray(exerciseBlueprint)
    ? exerciseBlueprint
    : exerciseBlueprint?.recommended_exercises || [];
  const warmup = Array.isArray(exerciseBlueprint?.warmup) ? exerciseBlueprint.warmup : [];
  const cooldown = Array.isArray(exerciseBlueprint?.cooldown) ? exerciseBlueprint.cooldown : [];
  const safetyNotes = Array.isArray(exerciseBlueprint?.safety_notes) ? exerciseBlueprint.safety_notes : [];
  const swaps = Array.isArray(exerciseBlueprint?.exercise_swaps) ? exerciseBlueprint.exercise_swaps : [];
  const weeklyStructure = exerciseBlueprint?.weekly_structure;

  return (
    <Stack spacing={1.5}>
      {/* NUTRITION RECOMMENDATIONS */}
      <Card
        sx={{
          borderRadius: "14px",
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
          color: isDark ? "#f8f6f0" : "#1A1A1A",
          p: 2,
          cursor: "pointer",
          transition: "all 0.3s ease",
          "&:hover": {
            borderColor: accentColor,
          },
        }}
        onClick={() => toggleSection("nutrition")}
      >
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <TrendingUpIcon sx={{ color: accentColor }} />
            <Typography sx={{ fontWeight: 700, fontSize: "1.05rem" }}>
              Personalized Daily Nutrition
            </Typography>
          </Stack>
        </Stack>

        {expandedSections["nutrition"] && (
          <Box sx={{ mt: 1.2 }}>
            <Grid container spacing={1}>
              <Grid size={{ xs: 6, sm: 3 }}>
                <Paper
                  sx={{
                    p: 1.2,
                    background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.4 }}>
                    Calories
                  </Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: "1.2rem", color: accentColor }}>
                    {dailyCalories}
                  </Typography>
                  <Typography sx={{ fontSize: "0.75rem", color: "rgba(120,120,120,1)" }}>
                    kcal/day
                  </Typography>
                </Paper>
              </Grid>

              <Grid size={{ xs: 6, sm: 3 }}>
                <Paper
                  sx={{
                    p: 1.2,
                    background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.4 }}>
                    Protein
                  </Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: "1.2rem", color: accentColor }}>
                    {nutrition?.protein_grams || 0}g
                  </Typography>
                  <Typography sx={{ fontSize: "0.75rem", color: "rgba(120,120,120,1)" }}>
                    per day
                  </Typography>
                </Paper>
              </Grid>

              <Grid size={{ xs: 6, sm: 3 }}>
                <Paper
                  sx={{
                    p: 1.2,
                    background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.4 }}>
                    Carbs
                  </Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: "1.2rem", color: accentColor }}>
                    {nutrition?.carbs_grams || 0}g
                  </Typography>
                  <Typography sx={{ fontSize: "0.75rem", color: "rgba(120,120,120,1)" }}>
                    per day
                  </Typography>
                </Paper>
              </Grid>

              <Grid size={{ xs: 6, sm: 3 }}>
                <Paper
                  sx={{
                    p: 1.2,
                    background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.4 }}>
                    Fats
                  </Typography>
                  <Typography sx={{ fontWeight: 700, fontSize: "1.2rem", color: accentColor }}>
                    {nutrition?.fat_grams || 0}g
                  </Typography>
                  <Typography sx={{ fontSize: "0.75rem", color: "rgba(120,120,120,1)" }}>
                    per day
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            {/* MACRO PERCENTAGES */}
            <Box sx={{ mt: 1.4 }}>
              <Typography sx={{ fontSize: "0.9rem", fontWeight: 700, mb: 0.8, color: accentColor }}>
                Macro Distribution
              </Typography>
              <Stack spacing={0.8}>
                <Box>
                  <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.3 }}>
                    <Typography sx={{ fontSize: "0.85rem" }}>Protein</Typography>
                    <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                      {nutrition?.protein_percentage || 30}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={nutrition?.protein_percentage || 30}
                    sx={{
                      height: "6px",
                      borderRadius: "3px",
                      background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                      "& .MuiLinearProgress-bar": {
                        background: "#FF6B6B",
                      },
                    }}
                  />
                </Box>

                <Box>
                  <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.3 }}>
                    <Typography sx={{ fontSize: "0.85rem" }}>Carbs</Typography>
                    <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                      {nutrition?.carbs_percentage || 45}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={nutrition?.carbs_percentage || 45}
                    sx={{
                      height: "6px",
                      borderRadius: "3px",
                      background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                      "& .MuiLinearProgress-bar": {
                        background: "#4ECDC4",
                      },
                    }}
                  />
                </Box>

                <Box>
                  <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.3 }}>
                    <Typography sx={{ fontSize: "0.85rem" }}>Fats</Typography>
                    <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                      {nutrition?.fat_percentage || 25}%
                    </Typography>
                  </Stack>
                  <LinearProgress
                    variant="determinate"
                    value={nutrition?.fat_percentage || 25}
                    sx={{
                      height: "6px",
                      borderRadius: "3px",
                      background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                      "& .MuiLinearProgress-bar": {
                        background: "#FFD93D",
                      },
                    }}
                  />
                </Box>
              </Stack>
            </Box>
          </Box>
        )}
      </Card>

      {/* WORKOUT BLUEPRINT */}
      <Card
        sx={{
          borderRadius: "14px",
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
          color: isDark ? "#f8f6f0" : "#1A1A1A",
          p: 2,
        }}
      >
        <Typography sx={{ fontWeight: 700, fontSize: "1.05rem", mb: 0.5 }}>
          Smart Workout Blueprint
        </Typography>
        <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.75)" : "rgba(0, 0, 0, 0.7)", mb: 1.2 }}>
          Built from goal, equipment, injury context, and recent performance.
        </Typography>

        {weeklyStructure && (
          <Paper
            sx={{
              p: 1.2,
              mb: 1.2,
              borderRadius: "10px",
              background: isDark ? "rgba(212,175,55,0.08)" : "rgba(43, 95, 58, 0.06)",
            }}
          >
            <Typography sx={{ fontSize: "0.9rem", fontWeight: 700, mb: 0.4 }}>
              Weekly Structure
            </Typography>
            <Typography sx={{ fontSize: "0.86rem", mb: 0.2 }}>
              {weeklyStructure.sessions_per_week} sessions per week
            </Typography>
            <Typography sx={{ fontSize: "0.86rem" }}>
              Focus: {String(weeklyStructure.focus || "balanced training")}
            </Typography>
          </Paper>
        )}

        {!!warmup.length && (
          <Box sx={{ mb: 1.2 }}>
            <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>
              Warmup
            </Typography>
            {warmup.slice(0, 4).map((item: string, idx: number) => (
              <Typography key={`warmup-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>
                • {item}
              </Typography>
            ))}
          </Box>
        )}

        <Stack spacing={0.8}>
          {exercises.slice(0, 6).map((exercise, idx: number) => {
            const exerciseRecord = exercise as ExerciseRecommendation;
            return (
              <Paper
                key={`${exerciseRecord?.id ?? idx}`}
                sx={{
                  p: 1.1,
                  borderRadius: "10px",
                  background: isDark ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.6)",
                  border: isDark ? "1px solid rgba(255,255,255,0.06)" : "1px solid rgba(0,0,0,0.04)",
                }}
              >
                <Stack direction="row" justifyContent="space-between" spacing={1} sx={{ mb: 0.4 }}>
                  <Typography sx={{ fontWeight: 700, fontSize: "0.92rem" }}>
                    {String(exerciseRecord?.name ?? exerciseRecord?.title ?? String(exerciseRecord)).replace(/_/g, " ")}
                  </Typography>
                  {typeof exerciseRecord?.score === "number" && (
                    <Chip
                      size="small"
                      label={`${Math.round((exerciseRecord.score as number) * 10) / 10}`}
                      sx={{ height: 22, fontSize: "0.72rem", background: accentColor, color: isDark ? "#111" : "#fff" }}
                    />
                  )}
                </Stack>
                <Typography sx={{ fontSize: "0.82rem", color: isDark ? "rgba(248,246,240,0.76)" : "rgba(0, 0, 0, 0.68)", mb: 0.3 }}>
                  {String(exerciseRecord?.sets_reps ?? exerciseRecord?.phase ?? "Main work")}
                </Typography>
                <Typography sx={{ fontSize: "0.8rem", color: isDark ? "rgba(248,246,240,0.68)" : "rgba(0, 0, 0, 0.62)" }}>
                  {String(exerciseRecord?.why ?? exerciseRecord?.description ?? "Selected for balanced progression.")}
                </Typography>
              </Paper>
            );
          })}
        </Stack>

        {!!safetyNotes.length && (
          <Box sx={{ mt: 1.2 }}>
            <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>
              Safety Notes
            </Typography>
            {safetyNotes.slice(0, 4).map((item: string, idx: number) => (
              <Typography key={`safety-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>
                • {item}
              </Typography>
            ))}
          </Box>
        )}

        {!!swaps.length && (
          <Box sx={{ mt: 1.2 }}>
            <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>
              Safer Substitutions
            </Typography>
            {swaps.slice(0, 4).map((item, idx: number) => {
              const swapItem = item as SwapRecommendation;
              return (
                <Typography key={`swap-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>
                  • {String(swapItem.exercise ?? "")} → {String(swapItem.safer_alternative ?? "")}
                </Typography>
              );
            })}
          </Box>
        )}

        {!!cooldown.length && (
          <Box sx={{ mt: 1.2 }}>
            <Typography sx={{ fontSize: "0.85rem", fontWeight: 700, color: accentColor, mb: 0.4 }}>
              Cooldown
            </Typography>
            {cooldown.slice(0, 4).map((item: string, idx: number) => (
              <Typography key={`cooldown-${idx}`} sx={{ fontSize: "0.84rem", color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0, 0, 0, 0.68)" }}>
                • {item}
              </Typography>
            ))}
          </Box>
        )}
      </Card>

      {/* GOAL ACHIEVEMENT */}
      <Card
        sx={{
          borderRadius: "14px",
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
          color: isDark ? "#f8f6f0" : "#1A1A1A",
          p: 2,
          cursor: "pointer",
          transition: "all 0.3s ease",
          "&:hover": {
            borderColor: accentColor,
          },
        }}
        onClick={() => toggleSection("goals")}
      >
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <CheckCircleIcon sx={{ color: accentColor }} />
            <Typography sx={{ fontWeight: 700, fontSize: "1.05rem" }}>
              Goal Achievement Prediction
            </Typography>
          </Stack>
        </Stack>

        {expandedSections["goals"] && (
          <Box sx={{ mt: 1.2 }}>
            <Stack spacing={1}>
              <Paper
                sx={{
                  p: 1.4,
                  background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                  borderRadius: "8px",
                }}
              >
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 0.8 }}>
                  <Typography sx={{ fontSize: "0.9rem", fontWeight: 700 }}>
                    Success Probability
                  </Typography>
                  <Chip
                    label={`${Math.round((goalData?.success_probability || 0) * 100)}%`}
                    sx={{
                      background: accentColor,
                      color: isDark ? "#111" : "#fff",
                      fontWeight: 700,
                    }}
                  />
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={(goalData?.success_probability || 0) * 100}
                  sx={{
                    height: "8px",
                    borderRadius: "4px",
                    background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                    "& .MuiLinearProgress-bar": {
                      background: accentColor,
                    },
                  }}
                />
              </Paper>

              <Stack
                direction="row"
                spacing={1}
                sx={{
                  p: 1.2,
                  background: isDark ? "rgba(255,255,255,0.04)" : "rgba(0, 0, 0, 0.02)",
                  borderRadius: "8px",
                }}
              >
                <InfoIcon sx={{ color: accentColor, fontSize: "1.2rem", flexShrink: 0 }} />
                <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)" }}>
                  {goalData?.recommendation || "Keep up your consistency for better results"}
                </Typography>
              </Stack>
            </Stack>
          </Box>
        )}
      </Card>

      {/* RECOMMENDED EXERCISES */}
      <Card
        sx={{
          borderRadius: "14px",
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
          color: isDark ? "#f8f6f0" : "#1A1A1A",
          p: 2,
        }}
      >
        <Typography sx={{ fontWeight: 700, fontSize: "1.05rem", mb: 1 }}>
          🏋️ AI-Recommended Exercises
        </Typography>
        <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.75)" : "rgba(0, 0, 0, 0.7)", mb: 1.2 }}>
          Based on your goal, preferences, and training constraints
        </Typography>

        <Stack direction="row" spacing={1} sx={{ flexWrap: "wrap" }}>
          {exercises && exercises.length > 0 ? (
            exercises.slice(0, 8).map((exercise, idx: number) => {
              const exerciseRecord = exercise as ExerciseRecommendation;
              return (
                <Chip
                  key={idx}
                  label={String(exerciseRecord?.name ?? exerciseRecord?.title ?? String(exerciseRecord)).replace(/_/g, " ")}
                  sx={{
                    background: isDark ? "rgba(212,175,55,0.15)" : "rgba(43, 95, 58, 0.1)",
                    color: accentColor,
                    fontWeight: 600,
                    borderRadius: "20px",
                  }}
                />
              );
            })
          ) : (
            <Typography sx={{ fontSize: "0.9rem" }}>Loading recommendations...</Typography>
          )}
        </Stack>
      </Card>

      {/* ML DISCLAIMER */}
      <Alert
        severity="info"
        icon={<InfoIcon />}
        sx={{
          borderRadius: "10px",
          background: isDark ? "rgba(100,150,200,0.1)" : "rgba(100,150,200,0.05)",
          borderColor: isDark ? "rgba(100,150,200,0.2)" : "rgba(100,150,200,0.1)",
        }}
      >
        <Typography sx={{ fontSize: "0.85rem" }}>
          <strong>ML-Powered Insights:</strong> These recommendations are generated using machine learning based on your profile. Accuracy improves as you provide more feedback and workout data.
        </Typography>
      </Alert>
    </Stack>
  );
};

export default MLRecommendationsPanel;
