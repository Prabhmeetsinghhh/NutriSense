import { useMemo, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import {
  Alert,
  Box,
  Button,
  Checkbox,
  CircularProgress,
  Container,
  FormControlLabel,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useTheme } from "../context/ThemeContext";
import { getTheme } from "../theme/indianTheme";
import axios from "../api/axiosInstance";

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const SignupPage = () => {
  const navigate = useNavigate();
  const { theme: currentTheme } = useTheme();
  const themeConfig = getTheme(currentTheme);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [serverError, setServerError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const emailError = useMemo(() => {
    if (!isSubmitted && !email) return "";
    if (!email.trim()) return "Email is required";
    if (!emailPattern.test(email.trim())) return "Enter a valid email address";
    return "";
  }, [email, isSubmitted]);

  const passwordError = useMemo(() => {
    if (!isSubmitted && !password) return "";
    if (!password) return "Password is required";
    if (password.length < 8) return "Password must be at least 8 characters";
    return "";
  }, [password, isSubmitted]);

  const nameError = useMemo(() => {
    if (!isSubmitted && !name) return "";
    if (!name.trim()) return "Name is required";
    return "";
  }, [name, isSubmitted]);

  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const isPasswordStrong = password.length >= 8 && hasUppercase && hasLowercase && hasNumber;
  const isFormValid = !emailError && !passwordError && !nameError && !!name && !!email && !!password;

  const handleKeyDown = (event: KeyboardEvent<HTMLFormElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      void handleSignup();
    }
  };

  const handleSignup = async () => {
    setIsSubmitted(true);
    setServerError("");
    setSuccessMessage("");

    if (!isFormValid || isLoading) {
      return;
    }

    try {
      setIsLoading(true);
      const response = await axios.post("/auth/signup", {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        password,
      });
      setSuccessMessage(response.data.message || "Account created successfully.");
      setTimeout(() => {
        navigate("/login");
      }, 900);
    } catch (error: unknown) {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
        "Signup failed. Please try again.";
      setServerError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    void handleSignup();
  };

  const isDark = currentTheme === "dark";
  const accentColor = isDark ? "#FACC15" : "#2B5F3A";

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100vw",
        position: "relative",
        overflow: "hidden",
        backgroundColor: themeConfig.colors.bgDark,
        fontFamily: "'Poppins', 'Inter', sans-serif",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "background-color 0.3s ease",
      }}
    >
      <Container maxWidth="sm" sx={{ position: "relative", zIndex: 1, py: 4 }}>
        <Box
          component="form"
          onSubmit={handleSubmit}
          noValidate
          onKeyDown={handleKeyDown}
          sx={{
            background: isDark ? "rgba(15, 15, 15, 0.9)" : "rgba(255, 255, 255, 0.94)",
            border: isDark ? "1px solid rgba(250, 204, 21, 0.28)" : "1px solid rgba(0, 0, 0, 0.1)",
            backdropFilter: "blur(14px)",
            borderRadius: "20px",
            boxShadow: themeConfig.shadows.medium,
            p: { xs: 3, sm: 4 },
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: "1.8rem", sm: "2.2rem" },
              fontWeight: 800,
              color: accentColor,
              mb: 1,
            }}
          >
            Create Your NutriSense Account
          </Typography>
          <Typography sx={{ color: isDark ? "rgba(255,255,255,0.78)" : "rgba(0,0,0,0.7)", mb: 3 }}>
            Sign up to save your plans, progress, and get personalized recommendations.
          </Typography>

          {serverError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {serverError}
            </Alert>
          )}
          {successMessage && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {successMessage}
            </Alert>
          )}

          <TextField
            fullWidth
            label="Full Name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            error={!!nameError}
            helperText={nameError || "Enter your full name"}
            margin="normal"
            InputProps={{
              sx: {
                color: isDark ? "#f8f6f0" : "#1A1A1A",
                backgroundColor: isDark ? "rgba(18,18,18,0.72)" : "rgba(255,255,255,0.78)",
              },
            }}
          />
          <TextField
            fullWidth
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            error={!!emailError}
            helperText={emailError || "Use the email linked with your account"}
            margin="normal"
            InputProps={{
              sx: {
                color: isDark ? "#f8f6f0" : "#1A1A1A",
                backgroundColor: isDark ? "rgba(18,18,18,0.72)" : "rgba(255,255,255,0.78)",
              },
            }}
          />
          <TextField
            fullWidth
            label="Password"
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            error={!!passwordError}
            helperText={passwordError || (isPasswordStrong ? "Strong password format detected" : "Minimum 8 characters")}
            margin="normal"
            InputProps={{
              sx: {
                color: isDark ? "#f8f6f0" : "#1A1A1A",
                backgroundColor: isDark ? "rgba(18,18,18,0.72)" : "rgba(255,255,255,0.78)",
              },
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={() => setShowPassword((prev) => !prev)} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <FormControlLabel
            control={<Checkbox checked={rememberMe} onChange={(event) => setRememberMe(event.target.checked)} />}
            label="Remember me"
            sx={{ color: isDark ? "rgba(255,255,255,0.78)" : "rgba(0,0,0,0.75)", mt: 1 }}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={isLoading}
            sx={{
              mt: 2,
              py: 1.4,
              fontWeight: 700,
              backgroundColor: accentColor,
              color: "#111",
              '&:hover': { backgroundColor: isDark ? '#e4b30b' : '#214c2e' },
            }}
          >
            {isLoading ? <CircularProgress size={24} color="inherit" /> : "Create Account"}
          </Button>

          <Typography sx={{ mt: 2, fontSize: "0.95rem", textAlign: "center", color: isDark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.55)" }}>
            Already have an account?{' '}
            <Box
              component="span"
              onClick={() => navigate('/login')}
              sx={{ color: accentColor, cursor: 'pointer', textDecoration: 'underline' }}
            >
              Login
            </Box>
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default SignupPage;
