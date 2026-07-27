import { useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  Container,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { getTheme } from "../theme/indianTheme";

type FormData = {
  name: string;
  email: string;
  age: string;
  heightFeet: string;
  heightInches: string;
  weight: string;
  fitnessLevel: string;
  goal: string;
  dietType: string;
  budget_preference: string;
  injury_notes: string;
  avoid_exercises: string;
  equipment_access: string;
};

const initialForm: FormData = {
  name: "",
  email: "",
  age: "",
  heightFeet: "",
  heightInches: "",
  weight: "",
  fitnessLevel: "",
  goal: "",
  dietType: "",
  budget_preference: "",
  injury_notes: "",
  avoid_exercises: "",
  equipment_access: "",
};

const UserDetailsPage = () => {
  const navigate = useNavigate();
  const { theme: currentTheme } = useTheme();
  const themeConfig = getTheme(currentTheme);
  const isDark = currentTheme === "dark";
  const [formData, setFormData] = useState<FormData>(initialForm);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const getInputSx = () => ({
    "& .MuiOutlinedInput-root": {
      color: isDark ? "#f8f6f0" : "#1A1A1A",
      backgroundColor: isDark ? "rgba(18, 18, 18, 0.66)" : "rgba(255, 255, 255, 0.5)",
      borderRadius: "12px",
      "& fieldset": {
        borderColor: isDark
          ? "rgba(212, 175, 55, 0.35)"
          : "rgba(43, 95, 58, 0.25)",
      },
      "&:hover fieldset": {
        borderColor: isDark
          ? "rgba(212, 175, 55, 0.7)"
          : "rgba(43, 95, 58, 0.6)",
      },
      "&.Mui-focused fieldset": {
        borderColor: isDark ? "#D4AF37" : "#2B5F3A",
        boxShadow: isDark
          ? "0 0 0 3px rgba(212, 175, 55, 0.12)"
          : "0 0 0 3px rgba(43, 95, 58, 0.12)",
      },
    },
    "& .MuiInputLabel-root": {
      color: isDark ? "rgba(248, 246, 240, 0.75)" : "rgba(0, 0, 0, 0.6)",
    },
    "& .MuiFormHelperText-root": {
      color: isDark ? "#f9a8a8" : "#E74C3C",
    },
  });

  const handleChange = (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
  };

  const validate = () => {
    const next: Record<string, string> = {};

    if (!formData.name.trim()) next.name = "Name is required";
    if (!formData.email.trim()) next.email = "Email is required";
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      next.email = "Enter a valid email";
    }

    const age = Number(formData.age);
    if (!formData.age) next.age = "Age is required";
    else if (!Number.isFinite(age) || age < 15 || age > 100) {
      next.age = "Age must be between 15 and 100";
    }

    const feet = Number(formData.heightFeet);
    const inches = Number(formData.heightInches);
    if (!formData.heightFeet || !formData.heightInches) {
      next.height = "Height is required";
    } else if (!Number.isFinite(feet) || feet < 3 || feet > 8) {
      next.heightFeet = "Feet should be between 3 and 8";
    } else if (!Number.isFinite(inches) || inches < 0 || inches > 11) {
      next.heightInches = "Inches should be between 0 and 11";
    }

    const weight = Number(formData.weight);
    if (!formData.weight) next.weight = "Weight is required";
    else if (!Number.isFinite(weight) || weight < 30 || weight > 300) {
      next.weight = "Weight must be between 30 and 300 kg";
    }

    if (!formData.fitnessLevel) next.fitnessLevel = "Select your experience";
    if (!formData.goal) next.goal = "Select your goal";
    if (!formData.dietType) next.dietType = "Select your diet type";
    if (!formData.budget_preference) next.budget_preference = "Select your budget";

    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const isFormComplete = useMemo(
    () => {
      const requiredFields: Array<keyof FormData> = [
        "name",
        "email",
        "age",
        "heightFeet",
        "heightInches",
        "weight",
        "fitnessLevel",
        "goal",
        "dietType",
        "budget_preference",
      ];

      return requiredFields.every((field) => formData[field].trim().length > 0) && Object.keys(errors).length === 0;
    },
    [errors, formData]
  );

  const handleGenerate = async () => {
    if (!validate()) return;

    setIsLoading(true);
    const dataToSend = {
      ...formData,
      age: parseInt(formData.age, 10),
      heightFeet: parseInt(formData.heightFeet, 10),
      heightInches: parseInt(formData.heightInches, 10),
      weight: parseInt(formData.weight, 10),
    };

    setTimeout(() => {
      setIsLoading(false);
      navigate("/result", { state: dataToSend });
    }, 900);
  };

  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        py: { xs: 2.5, md: 4.5 },
        background: isDark
          ? "radial-gradient(circle at 15% 10%, rgba(212,175,55,0.18) 0%, rgba(212,175,55,0) 32%), linear-gradient(120deg, #070707 0%, #121016 55%, #17120f 100%)"
          : "linear-gradient(120deg, #F5F1E8 0%, #FAFAF8 55%, #F8F6F1 100%)",
        color: themeConfig.colors.textPrimary,
        position: "relative",
        overflow: "hidden",
        transition: "background 0.3s ease",
      }}
    >
      <style>
        {`@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Poppins:wght@400;500;600&display=swap');`}
      </style>

      <Box
        sx={{
          position: "absolute",
          inset: 0,
          background: isDark
            ? "linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.65)), repeating-linear-gradient(90deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 34px)"
            : "linear-gradient(180deg, rgba(255,255,255,0.5), rgba(255,255,255,0.3)), repeating-linear-gradient(90deg, rgba(0,0,0,0.01) 0px, rgba(0,0,0,0.01) 1px, transparent 1px, transparent 34px)",
          pointerEvents: "none",
        }}
      />

      <Container maxWidth="md" sx={{ position: "relative", zIndex: 1 }}>
        <Card
          sx={{
            borderRadius: "22px",
            border: isDark
              ? "1px solid rgba(212, 175, 55, 0.35)"
              : "1px solid rgba(43, 95, 58, 0.2)",
            background: isDark
              ? "rgba(14, 14, 16, 0.78)"
              : "rgba(255, 255, 255, 0.9)",
            backdropFilter: "blur(10px)",
            boxShadow: themeConfig.shadows.medium,
            p: { xs: 2.2, sm: 3.2, md: 4 },
            position: "relative",
            overflow: "hidden",
            transition: "all 0.3s ease",
            "&::before": {
              content: '""',
              position: "absolute",
              inset: 0,
              background: isDark
                ? "linear-gradient(140deg, rgba(212,175,55,0.06), transparent 45%)"
                : "linear-gradient(140deg, rgba(43,95,58,0.06), transparent 45%)",
              pointerEvents: "none",
            },
          }}
        >
          <Typography
            sx={{
              fontFamily: "'Cinzel', serif",
              fontSize: { xs: "1.8rem", md: "2.35rem" },
              color: accentColor,
              letterSpacing: "0.04em",
              textAlign: "center",
              mb: 0.8,
              transition: "color 0.3s ease",
            }}
          >
            Build Your Personalized Plan
          </Typography>

          <Typography
            sx={{
              fontFamily: "'Poppins', sans-serif",
              textAlign: "center",
              color: isDark ? "rgba(248, 246, 240, 0.82)" : "rgba(0, 0, 0, 0.7)",
              mb: 3,
              transition: "color 0.3s ease",
            }}
          >
            Share your details so NutriSense can create a practical and affordable plan.
          </Typography>

          {errors.height && (
            <Alert severity="error" sx={{ mb: 2.2, borderRadius: "10px" }}>
              {errors.height}
            </Alert>
          )}

          <Stack spacing={2.2}>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
                gap: 1.8,
              }}
            >
              <TextField
                label="Full Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                error={!!errors.name}
                helperText={errors.name}
                sx={getInputSx()}
              />
              <TextField
                label="Email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                error={!!errors.email}
                helperText={errors.email}
                sx={getInputSx()}
              />
            </Box>

            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "repeat(3, 1fr)" },
                gap: 1.8,
              }}
            >
              <TextField
                label="Age"
                name="age"
                value={formData.age}
                onChange={handleChange}
                error={!!errors.age}
                helperText={errors.age}
                sx={getInputSx()}
              />
              <TextField
                label="Height (feet)"
                name="heightFeet"
                value={formData.heightFeet}
                onChange={handleChange}
                error={!!errors.heightFeet}
                helperText={errors.heightFeet}
                sx={getInputSx()}
              />
              <TextField
                label="Height (inches)"
                name="heightInches"
                value={formData.heightInches}
                onChange={handleChange}
                error={!!errors.heightInches}
                helperText={errors.heightInches}
                sx={getInputSx()}
              />
            </Box>

            <TextField
              label="Weight (kg)"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
              error={!!errors.weight}
              helperText={errors.weight}
              sx={getInputSx()}
            />

            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
                gap: 1.8,
              }}
            >
              <TextField
                select
                label="Experience Level"
                name="fitnessLevel"
                value={formData.fitnessLevel}
                onChange={handleChange}
                error={!!errors.fitnessLevel}
                helperText={errors.fitnessLevel || "Amateur, Intermediate, or Professional"}
                sx={getInputSx()}
              >
                <MenuItem value="amateur">Amateur</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="professional">Professional</MenuItem>
              </TextField>

              <TextField
                select
                label="Goal"
                name="goal"
                value={formData.goal}
                onChange={handleChange}
                error={!!errors.goal}
                helperText={errors.goal}
                sx={getInputSx()}
              >
                <MenuItem value="weight_loss">Fat Loss</MenuItem>
                <MenuItem value="muscle_gain">Muscle Gain</MenuItem>
                <MenuItem value="maintenance">Maintain Weight</MenuItem>
                <MenuItem value="muscle_endurance">Build Endurance</MenuItem>
              </TextField>
            </Box>

            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
                gap: 1.8,
              }}
            >
              <TextField
                select
                label="Diet Type"
                name="dietType"
                value={formData.dietType}
                onChange={handleChange}
                error={!!errors.dietType}
                helperText={errors.dietType}
                sx={getInputSx()}
              >
                <MenuItem value="veg">Vegetarian</MenuItem>
                <MenuItem value="eggetarian">Vegetarian + Eggs</MenuItem>
                <MenuItem value="non_veg">Non-Vegetarian</MenuItem>
                <MenuItem value="vegan">Vegan</MenuItem>
              </TextField>

              <TextField
                select
                label="Daily Budget"
                name="budget_preference"
                value={formData.budget_preference}
                onChange={handleChange}
                error={!!errors.budget_preference}
                helperText={errors.budget_preference || "Choose your daily spend range"}
                sx={getInputSx()}
              >
                <MenuItem value="affordable">Rs. 100-250/day</MenuItem>
                <MenuItem value="value">Rs. 250-350/day</MenuItem>
                <MenuItem value="balanced">Rs. 350-500/day</MenuItem>
                <MenuItem value="premium">Rs. 500+/day</MenuItem>
              </TextField>
            </Box>

            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
                gap: 1.8,
              }}
            >
              <TextField
                label="Injury or limitation notes"
                name="injury_notes"
                value={formData.injury_notes}
                onChange={handleChange}
                helperText="Example: disc bulge, shoulder pain, knee pain"
                multiline
                minRows={3}
                sx={getInputSx()}
              />
              <TextField
                label="Exercises to avoid"
                name="avoid_exercises"
                value={formData.avoid_exercises}
                onChange={handleChange}
                helperText="Example: deadlift, bent over row, overhead press"
                multiline
                minRows={3}
                sx={getInputSx()}
              />
            </Box>

            <TextField
              label="Equipment available"
              name="equipment_access"
              value={formData.equipment_access}
              onChange={handleChange}
              helperText="Example: dumbbells, barbell, bench, pull up bar. Separate with commas"
              sx={getInputSx()}
            />

            <Box sx={{ pt: 1.2, display: "flex", gap: 1.2, flexWrap: "wrap" }}>
              <Button
                variant="outlined"
                onClick={() => navigate("/login")}
                sx={{
                  borderColor: isDark ? "rgba(255,255,255,0.42)" : "rgba(0,0,0,0.2)",
                  color: isDark ? "#f8f6f0" : "#1A1A1A",
                  textTransform: "none",
                  borderRadius: "999px",
                  px: 2.4,
                  backdropFilter: "blur(2px)",
                  transition: "all 0.3s ease",
                  "&:hover": {
                    borderColor: accentColor,
                    backgroundColor: isDark
                      ? "rgba(212, 175, 55, 0.08)"
                      : "rgba(43, 95, 58, 0.08)",
                    transform: "translateY(-1px)",
                  },
                }}
              >
                Back
              </Button>
              <Button
                variant="contained"
                onClick={handleGenerate}
                disabled={isLoading || !isFormComplete}
                sx={{
                  textTransform: "none",
                  borderRadius: "999px",
                  px: 3,
                  fontWeight: 600,
                  bgcolor: accentColor,
                  color: isDark ? "#151515" : "#FFFFFF",
                  boxShadow: isDark
                    ? "0 10px 28px rgba(212,175,55,0.25)"
                    : "0 10px 28px rgba(43,95,58,0.22)",
                  transition: "all 0.3s ease",
                  "&:hover": {
                    bgcolor: isDark ? "#E5C45F" : "#214C2E",
                    transform: "translateY(-2px)",
                  },
                  "&.Mui-disabled": {
                    bgcolor: isDark
                      ? "rgba(212, 175, 55, 0.4)"
                      : "rgba(43, 95, 58, 0.4)",
                    color: isDark ? "rgba(21, 21, 21, 0.65)" : "rgba(255, 255, 255, 0.65)",
                  },
                }}
              >
                {isLoading ? "Generating..." : "Generate My Plan"}
              </Button>
            </Box>
          </Stack>
        </Card>
      </Container>
    </Box>
  );
};

export default UserDetailsPage;


