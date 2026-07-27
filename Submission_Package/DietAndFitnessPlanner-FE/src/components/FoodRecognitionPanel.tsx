import { useState } from "react";
import {
  Card,
  Typography,
  Box,
  Stack,
  Button,
  TextField,
  Paper,
  Chip,
  CircularProgress,
  Alert,
  Grid,
  LinearProgress,
} from "@mui/material";
import {
  PhotoCamera as PhotoCameraIcon,
  TextFields as TextFieldsIcon,
} from "@mui/icons-material";
import axios from "../api/axiosInstance";

interface FoodRecognitionPanelProps {
  isDark: boolean;
}

interface NutritionEstimate {
  food_description: string;
  estimated_macros: {
    protein: number;
    carbs: number;
    fat: number;
    calories: number;
  };
  confidence: number;
}

const FoodRecognitionPanel = ({ isDark }: FoodRecognitionPanelProps) => {
  const [activeMode, setActiveMode] = useState<"text" | "image">("text");
  const [foodDescription, setFoodDescription] = useState("");
  const [nutrition, setNutrition] = useState<NutritionEstimate | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  const handleTextAnalysis = async () => {
    if (!foodDescription.trim()) {
      setError("Please describe what you ate");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("/ml/nutrition-from-text", {
        food_description: foodDescription,
      });

      if (response.data.status === "success") {
        setNutrition(response.data);
      } else {
        setError("Failed to analyze nutrition");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Error analyzing food. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await axios.post("/ml/food-recognition", {
        image_path: file.name,
      });

      if (response.data.status === "success") {
        setNutrition(response.data);
      } else {
        setError("Failed to recognize food from image");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Error processing image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getMacroColor = (macro: string) => {
    const colors: Record<string, string> = {
      protein: "#FF6B6B",
      carbs: "#4ECDC4",
      fat: "#FFD93D",
      calories: accentColor,
    };
    return colors[macro] || accentColor;
  };

  return (
    <Stack spacing={1.8}>
      <Card
        sx={{
          borderRadius: "14px",
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
          color: isDark ? "#f8f6f0" : "#1A1A1A",
          p: 2.2,
        }}
      >
        <Typography sx={{ fontWeight: 700, fontSize: "1.15rem", mb: 1.2 }}>
          🔍 Food Recognition & Nutrition Analyzer
        </Typography>

        <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)", mb: 1.4 }}>
          Get instant nutrition estimates from photos or text descriptions
        </Typography>

        {/* MODE SELECTION */}
        <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
          <Button
            variant={activeMode === "text" ? "contained" : "outlined"}
            startIcon={<TextFieldsIcon />}
            onClick={() => setActiveMode("text")}
            sx={{
              background: activeMode === "text" ? accentColor : "transparent",
              color: activeMode === "text" ? (isDark ? "#111" : "#fff") : accentColor,
              borderColor: accentColor,
              fontWeight: 600,
              flex: 1,
            }}
          >
            Text Description
          </Button>
          <Button
            variant={activeMode === "image" ? "contained" : "outlined"}
            startIcon={<PhotoCameraIcon />}
            onClick={() => setActiveMode("image")}
            sx={{
              background: activeMode === "image" ? accentColor : "transparent",
              color: activeMode === "image" ? (isDark ? "#111" : "#fff") : accentColor,
              borderColor: accentColor,
              fontWeight: 600,
              flex: 1,
            }}
          >
            Photo Upload
          </Button>
        </Stack>

        {/* TEXT MODE */}
        {activeMode === "text" && (
          <Stack spacing={1.2}>
            <TextField
              label="Describe what you ate"
              multiline
              rows={3}
              value={foodDescription}
              onChange={(e) => setFoodDescription(e.target.value)}
              placeholder="E.g., 2 cups of rice with grilled chicken breast and broccoli"
              fullWidth
              sx={{
                "& .MuiOutlinedInput-root": {
                  color: isDark ? "#f8f6f0" : "#1A1A1A",
                  background: isDark ? "rgba(255,255,255,0.04)" : "rgba(0, 0, 0, 0.02)",
                },
                "& .MuiOutlinedInput-notchedOutline": {
                  borderColor: isDark ? "rgba(212,175,55,0.2)" : "rgba(43, 95, 58, 0.1)",
                },
              }}
            />

            <Button
              variant="contained"
              onClick={handleTextAnalysis}
              disabled={loading || !foodDescription.trim()}
              sx={{
                background: accentColor,
                color: isDark ? "#111" : "#fff",
                fontWeight: 700,
                py: 1.2,
              }}
            >
              {loading ? <CircularProgress size={20} sx={{ mr: 1 }} /> : "Analyze Nutrition"}
            </Button>
          </Stack>
        )}

        {/* IMAGE MODE */}
        {activeMode === "image" && (
          <Stack spacing={1.2}>
            <Button
              component="label"
              variant="outlined"
              startIcon={<PhotoCameraIcon />}
              fullWidth
              sx={{
                borderColor: accentColor,
                color: accentColor,
                fontWeight: 600,
                py: 1.2,
                border: `2px dashed ${accentColor}`,
              }}
            >
              Upload Food Photo
              <input hidden accept="image/*" type="file" onChange={handleImageUpload} />
            </Button>

            {loading && (
              <Box sx={{ display: "flex", justifyContent: "center" }}>
                <CircularProgress sx={{ color: accentColor }} />
              </Box>
            )}

            <Typography sx={{ fontSize: "0.85rem", color: isDark ? "rgba(248,246,240,0.65)" : "rgba(0, 0, 0, 0.6)", textAlign: "center" }}>
              Supported: JPG, PNG, JPEG
            </Typography>
          </Stack>
        )}

        {/* ERROR MESSAGE */}
        {error && (
          <Alert severity="error" sx={{ mt: 1.2, borderRadius: "8px" }}>
            {error}
          </Alert>
        )}
      </Card>

      {/* NUTRITION RESULTS */}
      {nutrition && (
        <Card
          sx={{
            borderRadius: "14px",
            background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
            border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
            color: isDark ? "#f8f6f0" : "#1A1A1A",
            p: 2.2,
          }}
        >
          <Typography sx={{ fontWeight: 700, fontSize: "1.1rem", mb: 0.8 }}>
            📊 Estimated Nutrition
          </Typography>

          {nutrition.confidence && (
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1.2 }}>
              <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.7)" : "rgba(0, 0, 0, 0.6)" }}>
                Confidence Level
              </Typography>
              <Chip
                label={`${Math.round(nutrition.confidence * 100)}%`}
                sx={{
                  background: accentColor,
                  color: isDark ? "#111" : "#fff",
                  fontWeight: 700,
                }}
              />
            </Stack>
          )}

          {/* MACRO CARDS */}
          <Grid container spacing={1} sx={{ mb: 2 }}>
            <Grid size={{ xs: 6, sm: 3 }}>
              <Paper
                sx={{
                  p: 1.2,
                  background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                  borderRadius: "8px",
                  textAlign: "center",
                }}
              >
                <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.3 }}>
                  Calories
                </Typography>
                <Typography
                  sx={{ fontWeight: 700, fontSize: "1.3rem", color: getMacroColor("calories") }}
                >
                  {nutrition.estimated_macros.calories}
                </Typography>
                <Typography sx={{ fontSize: "0.7rem", color: "rgba(120,120,120,1)" }}>
                  kcal
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
                <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.3 }}>
                  Protein
                </Typography>
                <Typography
                  sx={{ fontWeight: 700, fontSize: "1.3rem", color: getMacroColor("protein") }}
                >
                  {nutrition.estimated_macros.protein}
                </Typography>
                <Typography sx={{ fontSize: "0.7rem", color: "rgba(120,120,120,1)" }}>
                  g
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
                <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.3 }}>
                  Carbs
                </Typography>
                <Typography
                  sx={{ fontWeight: 700, fontSize: "1.3rem", color: getMacroColor("carbs") }}
                >
                  {nutrition.estimated_macros.carbs}
                </Typography>
                <Typography sx={{ fontSize: "0.7rem", color: "rgba(120,120,120,1)" }}>
                  g
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
                <Typography sx={{ fontSize: "0.8rem", color: "rgba(120,120,120,1)", mb: 0.3 }}>
                  Fat
                </Typography>
                <Typography
                  sx={{ fontWeight: 700, fontSize: "1.3rem", color: getMacroColor("fat") }}
                >
                  {nutrition.estimated_macros.fat}
                </Typography>
                <Typography sx={{ fontSize: "0.7rem", color: "rgba(120,120,120,1)" }}>
                  g
                </Typography>
              </Paper>
            </Grid>
          </Grid>

          {/* MACRO BREAKDOWN BARS */}
          <Stack spacing={0.8}>
            <Box>
              <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.2 }}>
                <Typography sx={{ fontSize: "0.85rem" }}>Protein</Typography>
                <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                  {nutrition.estimated_macros.protein}g
                </Typography>
              </Stack>
              <LinearProgress
                variant="determinate"
                value={Math.min((nutrition.estimated_macros.protein / 100) * 100, 100)}
                sx={{
                  height: "6px",
                  borderRadius: "3px",
                  background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                  "& .MuiLinearProgress-bar": {
                    background: getMacroColor("protein"),
                  },
                }}
              />
            </Box>

            <Box>
              <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.2 }}>
                <Typography sx={{ fontSize: "0.85rem" }}>Carbs</Typography>
                <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                  {nutrition.estimated_macros.carbs}g
                </Typography>
              </Stack>
              <LinearProgress
                variant="determinate"
                value={Math.min((nutrition.estimated_macros.carbs / 100) * 100, 100)}
                sx={{
                  height: "6px",
                  borderRadius: "3px",
                  background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                  "& .MuiLinearProgress-bar": {
                    background: getMacroColor("carbs"),
                  },
                }}
              />
            </Box>

            <Box>
              <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.2 }}>
                <Typography sx={{ fontSize: "0.85rem" }}>Fats</Typography>
                <Typography sx={{ fontSize: "0.85rem", fontWeight: 700 }}>
                  {nutrition.estimated_macros.fat}g
                </Typography>
              </Stack>
              <LinearProgress
                variant="determinate"
                value={Math.min((nutrition.estimated_macros.fat / 100) * 100, 100)}
                sx={{
                  height: "6px",
                  borderRadius: "3px",
                  background: isDark ? "rgba(255,255,255,0.1)" : "rgba(0, 0, 0, 0.1)",
                  "& .MuiLinearProgress-bar": {
                    background: getMacroColor("fat"),
                  },
                }}
              />
            </Box>
          </Stack>

          <Alert severity="info" sx={{ mt: 1.2, borderRadius: "8px", fontSize: "0.85rem" }}>
            These are estimates. Actual values may vary. For best accuracy, refer to food packaging labels.
          </Alert>
        </Card>
      )}
    </Stack>
  );
};

export default FoodRecognitionPanel;
