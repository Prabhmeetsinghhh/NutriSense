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
import { useEffect, useMemo, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import { Check, Close, Visibility, VisibilityOff } from "@mui/icons-material";
import { useTheme } from "../context/ThemeContext";
import { getTheme } from "../theme/indianTheme";
import axios from "../api/axiosInstance";

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const rememberedEmailKey = "nutrisenseRememberedEmail";
const rememberMeKey = "nutrisenseRememberMe";
const defaultLeftImage = "/images/arnold.webp";
const defaultRightImage = "/images/Ronnie.webp";
const customLeftImage = "/images/login/login-left.jpg";
const customRightImage = "/images/login/login-right.jpg";

const resolveAvailableImage = (src: string, fallback: string): Promise<string> => {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(src);
    img.onerror = () => resolve(fallback);
    img.src = src;
  });
};

const LoginPage = () => {
  const navigate = useNavigate();
  const { theme: currentTheme } = useTheme();
  const themeConfig = getTheme(currentTheme);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [serverError, setServerError] = useState("");
  const [leftBgImage, setLeftBgImage] = useState(defaultLeftImage);
  const [rightBgImage, setRightBgImage] = useState(defaultRightImage);

  useEffect(() => {
    const savedRememberFlag = localStorage.getItem(rememberMeKey) === "true";
    const savedEmail = localStorage.getItem(rememberedEmailKey) ?? "";

    if (savedRememberFlag && savedEmail) {
      setRememberMe(true);
      setEmail(savedEmail);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    const loadCustomImages = async () => {
      const [resolvedLeft, resolvedRight] = await Promise.all([
        resolveAvailableImage(customLeftImage, defaultLeftImage),
        resolveAvailableImage(customRightImage, defaultRightImage),
      ]);

      if (isMounted) {
        setLeftBgImage(resolvedLeft);
        setRightBgImage(resolvedRight);
      }
    };

    void loadCustomImages();

    return () => {
      isMounted = false;
    };
  }, []);

  const emailError = useMemo(() => {
    if (!isSubmitted && !email) {
      return "";
    }
    if (!email.trim()) {
      return "Email is required";
    }
    if (!emailPattern.test(email.trim())) {
      return "Enter a valid email address";
    }
    return "";
  }, [email, isSubmitted]);

  const passwordError = useMemo(() => {
    if (!isSubmitted && !password) {
      return "";
    }
    if (!password) {
      return "Password is required";
    }
    if (password.length < 8) {
      return "Password must be at least 8 characters";
    }
    return "";
  }, [password, isSubmitted]);

  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const isPasswordStrong = password.length >= 8 && hasUppercase && hasLowercase && hasNumber;
  const isFormValid = !emailError && !passwordError && !!email && !!password;

  const handleKeyDown = (event: KeyboardEvent<HTMLFormElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      void handleLogin();
    }
  };

  const handleLogin = async () => {
    setIsSubmitted(true);
    setServerError("");

    if (!isFormValid || isLoading) {
      return;
    }

    try {
      setIsLoading(true);
      const normalizedEmail = email.trim().toLowerCase();
      const response = await axios.post("/auth/login", {
        email: normalizedEmail,
        password,
      });

      localStorage.setItem("nutrisenseUser", normalizedEmail);
      localStorage.setItem("nutrisenseAuth", JSON.stringify(response.data.user));

      if (rememberMe) {
        localStorage.setItem(rememberedEmailKey, normalizedEmail);
        localStorage.setItem(rememberMeKey, "true");
      } else {
        localStorage.removeItem(rememberedEmailKey);
        localStorage.setItem(rememberMeKey, "false");
      }

      window.dispatchEvent(new Event("nutrisense-auth-changed"));

      navigate("/details");
    } catch (error: unknown) {
      const message =
        (error as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
        "Login failed. Please try again.";
      setServerError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    void handleLogin();
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
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(24px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}
      </style>

      <Box
        sx={{
          position: "absolute",
          inset: 0,
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1.15fr 0.85fr" },
        }}
      >
        <Box
          sx={{
            display: { xs: "none", md: "block" },
            backgroundImage: `url('${leftBgImage}')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            filter: isDark ? "grayscale(100%)" : "grayscale(60%) brightness(1.05)",
            position: "relative",
            "&::after": {
              content: '""',
              position: "absolute",
              inset: 0,
              background: isDark
                ? "linear-gradient(100deg, rgba(10,10,10,0.9) 0%, rgba(10,10,10,0.5) 45%, rgba(10,10,10,0.25) 100%)"
                : "linear-gradient(100deg, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0.7) 45%, rgba(255,255,255,0.55) 100%)",
            },
          }}
        />

        <Box
          sx={{
            backgroundImage: {
              xs: isDark
                ? `linear-gradient(145deg, rgba(10,10,10,0.97), rgba(10,10,10,0.88)), url('${rightBgImage}')`
                : `linear-gradient(145deg, rgba(255,255,255,0.95), rgba(255,255,255,0.92)), url('${rightBgImage}')`,
              md: `url('${rightBgImage}')`,
            },
            backgroundSize: "cover",
            backgroundPosition: "center",
            filter: { md: isDark ? "grayscale(100%)" : "grayscale(60%) brightness(1.05)" },
            position: "relative",
            "&::after": {
              content: '""',
              position: "absolute",
              inset: 0,
              background: isDark
                ? {
                    xs: "linear-gradient(145deg, rgba(10,10,10,0.78), rgba(10,10,10,0.82))",
                    md: "linear-gradient(to left, rgba(10,10,10,0.86), rgba(10,10,10,0.55))",
                  }
                : {
                    xs: "linear-gradient(145deg, rgba(255,255,255,0.8), rgba(255,255,255,0.75))",
                    md: "linear-gradient(to left, rgba(255,255,255,0.7), rgba(255,255,255,0.5))",
                  },
            },
          }}
        />
      </Box>

      <Container
        maxWidth="sm"
        sx={{
          position: "relative",
          zIndex: 2,
          px: { xs: 2.5, sm: 3 },
          animation: "fadeInUp 0.7s ease-out",
        }}
      >
        <Box
          component="form"
          onSubmit={onSubmit}
          noValidate
          onKeyDown={handleKeyDown}
          sx={{
            background: isDark
              ? "rgba(15, 15, 15, 0.82)"
              : "rgba(255, 255, 255, 0.92)",
            border: isDark
              ? "1px solid rgba(250, 204, 21, 0.28)"
              : "1px solid rgba(0, 0, 0, 0.08)",
            backdropFilter: "blur(10px)",
            borderRadius: "18px",
            px: { xs: 2.5, sm: 4 },
            py: { xs: 3, sm: 4 },
            boxShadow: themeConfig.shadows.medium,
            position: "relative",
            overflow: "hidden",
            transition: "all 0.3s ease",
            "&::before": {
              content: '""',
              position: "absolute",
              inset: 0,
              background: isDark
                ? "linear-gradient(135deg, rgba(250,204,21,0.06), transparent 48%)"
                : "linear-gradient(135deg, rgba(43,95,58,0.07), transparent 48%)",
              pointerEvents: "none",
            },
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: "0.8rem", sm: "0.88rem" },
              letterSpacing: "0.16em",
              color:isDark ? "rgba(255,255,255,0.65)" : "rgba(0,0,0,0.55)",
              textTransform: "uppercase",
              mb: 1,
              transition: "color 0.3s ease",
            }}
          >
            {isDark ? (
              "NutriSense Access"
            ) : (
              <>
                <Box component="span" sx={{ color: "#2B5F3A" }}>
                  Nutri
                </Box>
                <Box component="span" sx={{ color: "#1A1A1A" }}>
                  Sense
                </Box>{" "}
                Access
              </>
            )}
          </Typography>

          <Typography
            sx={{
              fontSize: { xs: "1.85rem", sm: "2.2rem" },
              fontWeight: 800,
              color: accentColor,
              lineHeight: 1.15,
              mb: 1,
              transition: "color 0.3s ease",
            }}
          >
            Welcome back.
          </Typography>

          <Typography
            sx={{
              color: isDark ? "rgba(255,255,255,0.86)" : "rgba(0,0,0,0.7)",
              mb: 3,
              fontSize: { xs: "0.92rem", sm: "1rem" },
              transition: "color 0.3s ease",
            }}
          >
            Log in to continue your budget-friendly fitness journey.
          </Typography>
          {serverError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {serverError}
            </Alert>
          )}
          <Typography
            sx={{
              fontSize: "0.92rem",
              color: isDark ? "rgba(255,255,255,0.72)" : "rgba(0,0,0,0.6)",
              mb: 2,
              display: "block",
            }}
            >
              Don’t have an account?{' '}
              <Box
                component="span"
                onClick={() => navigate('/signup')}
                sx={{
                  color: accentColor,
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  '&:hover': { opacity: 0.85 },
                }}
              >
                Sign up
              </Box>
            </Typography>
          <TextField
            fullWidth
            label="Email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            error={!!emailError}
            helperText={emailError || "Use the email linked with your account"}
            margin="normal"
            autoComplete="email"
            InputProps={{
              endAdornment: email ? (
                <InputAdornment position="end">
                  {emailError ? <Close sx={{ color: "#ef5350" }} /> : <Check sx={{ color: "#4e9a60" }} />}
                </InputAdornment>
              ) : null,
            }}
            sx={{
              "& .MuiInputLabel-root": {
                color: isDark ? "rgba(255,255,255,0.72)" : "rgba(0,0,0,0.6)",
              },
              "& .MuiInputLabel-root.Mui-focused": {
                color: accentColor,
              },
              "& .MuiOutlinedInput-root": {
                color: isDark ? "#FFFFFF" : "#000000",
                background: isDark ? "rgba(255,255,255,0.03)" : "rgba(0,0,0,0.02)",
                "& fieldset": {
                  borderColor: isDark ? "rgba(255,255,255,0.26)" : "rgba(0,0,0,0.12)",
                },
                "&:hover fieldset": {
                  borderColor: isDark ? "rgba(250,204,21,0.65)" : "rgba(43,95,58,0.5)",
                },
                "&.Mui-focused fieldset": { borderColor: accentColor },
              },
              "& .MuiFormHelperText-root": {
                color: emailError
                  ? "#ff8a80"
                  : isDark
                  ? "rgba(255,255,255,0.55)"
                  : "rgba(0,0,0,0.56)",
                ml: 0.5,
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
            helperText={passwordError || "Minimum 8 characters"}
            margin="normal"
            autoComplete="current-password"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword((prev) => !prev)}
                    edge="end"
                    sx={{
                      color: isDark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.54)",
                    }}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
            sx={{
              "& .MuiInputLabel-root": {
                color: isDark ? "rgba(255,255,255,0.72)" : "rgba(0,0,0,0.6)",
              },
              "& .MuiInputLabel-root.Mui-focused": {
                color: accentColor,
              },
              "& .MuiOutlinedInput-root": {
                color: isDark ? "#FFFFFF" : "#000000",
                background: isDark ? "rgba(255,255,255,0.03)" : "rgba(0,0,0,0.02)",
                "& fieldset": {
                  borderColor: isDark ? "rgba(255,255,255,0.26)" : "rgba(0,0,0,0.12)",
                },
                "&:hover fieldset": {
                  borderColor: isDark ? "rgba(250,204,21,0.65)" : "rgba(43,95,58,0.5)",
                },
                "&.Mui-focused fieldset": { borderColor: accentColor },
              },
              "& .MuiFormHelperText-root": {
                color: passwordError
                  ? "#ff8a80"
                  : isDark
                  ? "rgba(255,255,255,0.55)"
                  : "rgba(0,0,0,0.56)",
                ml: 0.5,
              },
            }}
          />

          {password && (
            <Typography
              sx={{
                mt: 1,
                color: isPasswordStrong ? "#7ee787" : "#ffd166",
                fontSize: "0.84rem",
                letterSpacing: "0.02em",
              }}
            >
              {isPasswordStrong
                ? "Strong password format detected"
                : "Tip: include uppercase, lowercase and a number"}
            </Typography>
          )}

          <FormControlLabel
            control={
              <Checkbox
                checked={rememberMe}
                onChange={(event) => setRememberMe(event.target.checked)}
                sx={{
                  color: isDark ? "rgba(255,255,255,0.6)" : "rgba(0,0,0,0.54)",
                  "&.Mui-checked": {
                    color: accentColor,
                  },
                }}
              />
            }
            label="Remember me"
            sx={{
              mt: 0.6,
              userSelect: "none",
              "& .MuiFormControlLabel-label": {
                color: isDark ? "rgba(255,255,255,0.82)" : "rgba(0,0,0,0.8)",
                fontSize: "0.95rem",
              },
            }}
          />

          <Button
            fullWidth
            type="submit"
            disabled={isLoading}
            sx={{
              mt: 3,
              py: 1.35,
              fontSize: "1rem",
              fontWeight: 700,
              letterSpacing: "0.02em",
              textTransform: "none",
              color: isDark ? "#000000" : "#FFFFFF",
              borderRadius: "10px",
              backgroundColor: isDark ? "#FACC15" : "#2B5F3A",
              boxShadow: isDark
                ? "0 8px 28px rgba(250, 204, 21, 0.25)"
                : "0 8px 28px rgba(43, 95, 58, 0.25)",
              transition: "transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease",
              "&:hover": {
                backgroundColor: isDark ? "#EAB308" : "#214C2E",
                transform: "translateY(-2px)",
                boxShadow: isDark
                  ? "0 12px 32px rgba(250, 204, 21, 0.35)"
                  : "0 12px 32px rgba(43, 95, 58, 0.35)",
              },
              "&.Mui-disabled": {
                backgroundColor: isDark ? "rgba(250, 204, 21, 0.35)" : "rgba(43, 95, 58, 0.35)",
                color: isDark ? "rgba(0, 0, 0, 0.6)" : "rgba(255, 255, 255, 0.6)",
              },
            }}
          >
            {isLoading ? (
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <CircularProgress
                  size={18}
                  sx={{ color: isDark ? "#000000" : "#FFFFFF" }}
                />
                Logging in...
              </Box>
            ) : (
              "Login"
            )}
          </Button>

          <Button
            fullWidth
            variant="text"
            onClick={() => navigate("/")}
            sx={{
              mt: 1.4,
              color: isDark ? "rgba(255,255,255,0.85)" : "rgba(0,0,0,0.7)",
              textTransform: "none",
              fontWeight: 500,
              transition: "all 0.3s ease",
              "&:hover": {
                color: accentColor,
                background: isDark
                  ? "rgba(250,204,21,0.08)"
                  : "rgba(43, 95, 58, 0.08)",
              },
            }}
          >
            Back to Home
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default LoginPage;


