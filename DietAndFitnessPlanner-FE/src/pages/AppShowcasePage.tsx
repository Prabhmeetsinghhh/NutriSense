import {
  Box,
  Button,
  Chip,
  Container,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import RestaurantMenuRoundedIcon from "@mui/icons-material/RestaurantMenuRounded";
import FitnessCenterRoundedIcon from "@mui/icons-material/FitnessCenterRounded";
import InsightsRoundedIcon from "@mui/icons-material/InsightsRounded";
import LocalDiningRoundedIcon from "@mui/icons-material/LocalDiningRounded";
import AutoAwesomeRoundedIcon from "@mui/icons-material/AutoAwesomeRounded";
import BoltRoundedIcon from "@mui/icons-material/BoltRounded";
import ShieldRoundedIcon from "@mui/icons-material/ShieldRounded";
import { useTheme } from "../context/ThemeContext";
import { getTheme } from "../theme/indianTheme";

const AppShowcasePage = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const currentTheme = getTheme(theme);

  useEffect(() => {
    const nodes = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]"));

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("reveal-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 }
    );

    nodes.forEach((node) => observer.observe(node));

    return () => observer.disconnect();
  }, []);

  const cards = [
    {
      title: "Smart Indian Diet Plans",
      text: "Balanced meal plans based on your goals, preferences, and realistic daily routine.",
      icon: <RestaurantMenuRoundedIcon sx={{ fontSize: 28 }} />,
    },
    {
      title: "Simple Workout Guidance",
      text: "Beginner-friendly fitness suggestions that match your body target and available time.",
      icon: <FitnessCenterRoundedIcon sx={{ fontSize: 28 }} />,
    },
    {
      title: "Goal-Based Strategy",
      text: "The app combines your details to generate a practical plan for fat loss, muscle gain, or maintenance.",
      icon: <InsightsRoundedIcon sx={{ fontSize: 28 }} />,
    },
  ];

  const steps = [
    {
      title: "You Tell Us About You",
      text: "Share your goal, diet type, activity level, and budget in a simple flow.",
      icon: <AutoAwesomeRoundedIcon sx={{ fontSize: 22 }} />,
    },
    {
      title: "AI Builds Your Personal Plan",
      text: "NutriSense maps food + fitness logic into practical day-wise recommendations.",
      icon: <BoltRoundedIcon sx={{ fontSize: 22 }} />,
    },
    {
      title: "You Follow A Clear Roadmap",
      text: "Get actionable guidance that is realistic, affordable, and easy to continue.",
      icon: <ShieldRoundedIcon sx={{ fontSize: 22 }} />,
    },
  ];

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background:
          theme === "dark"
            ? "radial-gradient(circle at 20% 20%, #27213a 0%, #16131f 40%, #0f0d16 100%)"
            : "radial-gradient(circle at 15% 20%, #fff9ef 0%, #fef3da 45%, #f8eee1 100%)",
        color: currentTheme.colors.textPrimary,
        py: { xs: 8, md: 10 },
        px: { xs: 2, md: 3 },
        transition: "all 0.3s ease",
      }}
    >
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

          .reveal-item {
            opacity: 0;
            transform: translateY(36px) scale(0.985);
            transition: opacity 680ms ease, transform 680ms ease;
            transition-delay: var(--reveal-delay, 0ms);
            will-change: transform, opacity;
          }

          .reveal-visible {
            opacity: 1;
            transform: translateY(0) scale(1);
          }

          .spotlight-sheen {
            position: relative;
            overflow: hidden;
          }

          .spotlight-sheen::after {
            content: "";
            position: absolute;
            top: -120%;
            left: -35%;
            width: 45%;
            height: 300%;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 50%, transparent 100%);
            transform: rotate(18deg);
            animation: sweep 5.8s linear infinite;
            pointer-events: none;
          }

          @keyframes sweep {
            from { transform: translateX(-20%) rotate(18deg); }
            to { transform: translateX(320%) rotate(18deg); }
          }
        `}
      </style>

      <Container maxWidth="lg">
        <Paper
          elevation={0}
          sx={{
            position: "relative",
            borderRadius: 4,
            overflow: "hidden",
            border:
              theme === "dark"
                ? "1px solid rgba(255,255,255,0.14)"
                : "1px solid rgba(0,0,0,0.08)",
            background:
              theme === "dark"
                ? "linear-gradient(135deg, rgba(27,22,39,0.9) 0%, rgba(17,16,27,0.93) 100%)"
                : "linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(255,247,232,0.96) 100%)",
            boxShadow: currentTheme.shadows.medium,
          }}
        >
          <Box
            sx={{
              position: "absolute",
              top: { xs: 14, md: 18 },
              right: { xs: 14, md: 20 },
              zIndex: 2,
            }}
          >
            <Button
              variant="outlined"
              onClick={() => navigate("/login")}
              sx={{
                textTransform: "none",
                borderRadius: 999,
                px: 2,
                py: 0.6,
                fontFamily: "'Manrope', sans-serif",
                fontWeight: 700,
                fontSize: { xs: "0.8rem", md: "0.88rem" },
                borderColor:
                  theme === "dark"
                    ? "rgba(255,255,255,0.4)"
                    : "rgba(0,0,0,0.22)",
                color: theme === "dark" ? "#f5efe2" : "#1A1A1A",
                backgroundColor:
                  theme === "dark"
                    ? "rgba(0,0,0,0.22)"
                    : "rgba(255,255,255,0.72)",
                boxShadow:
                  theme === "dark"
                    ? "0 8px 20px rgba(0,0,0,0.25)"
                    : "0 8px 20px rgba(0,0,0,0.12)",
                backdropFilter: "blur(3px)",
                "&:hover": {
                  borderColor:
                    theme === "dark"
                      ? "rgba(255,255,255,0.68)"
                      : "rgba(0,0,0,0.4)",
                  backgroundColor:
                    theme === "dark"
                      ? "rgba(255,255,255,0.08)"
                      : "rgba(255,255,255,0.95)",
                  transform: "translateY(-1px)",
                },
              }}
            >
              Login / Sign Up
            </Button>
          </Box>

          <Box sx={{ p: { xs: 3, md: 6 } }}>
              <Stack
                spacing={2}
                alignItems="center"
                textAlign="center"
                data-reveal
                className="reveal-item"
              >
              <Chip
                icon={<LocalDiningRoundedIcon />}
                label="What NutriSense Does"
                sx={{
                  fontFamily: "'Manrope', sans-serif",
                  fontWeight: 700,
                  backgroundColor:
                    theme === "dark"
                      ? "rgba(255,107,53,0.2)"
                      : "rgba(43,95,58,0.12)",
                  color: theme === "dark" ? "#ffd3c2" : "#2B5F3A",
                }}
              />

              <Typography
                sx={{
                  fontFamily: "'Cinzel', serif",
                  fontSize: { xs: "2rem", md: "3.1rem" },
                  fontWeight: 800,
                  letterSpacing: "0.03em",
                  lineHeight: 1.15,
                  color: theme === "dark" ? "#F4E6C2" : "#1A1A1A",
                }}
              >
                Build A Plan That Fits Real Life
              </Typography>

              <Typography
                sx={{
                  maxWidth: 760,
                  fontFamily: "'Manrope', sans-serif",
                  fontSize: { xs: "1rem", md: "1.1rem" },
                  lineHeight: 1.75,
                  color: currentTheme.colors.textSecondary,
                }}
              >
                NutriSense uses your details to generate a personalized Indian diet
                and fitness roadmap. You get structure, clarity, and practical
                actions instead of random advice.
              </Typography>
            </Stack>

            <Box
              data-reveal
              className="reveal-item"
              sx={{
                "--reveal-delay": "120ms",
                mt: { xs: 3, md: 4 },
                display: "grid",
                gap: 2.5,
                gridTemplateColumns: { xs: "1fr", md: "repeat(3, minmax(0, 1fr))" },
              }}
            >
              {cards.map((card) => (
                <Box key={card.title}>
                  <Paper
                    elevation={0}
                    sx={{
                      p: 2.5,
                      height: "100%",
                      borderRadius: 3,
                      border:
                        theme === "dark"
                          ? "1px solid rgba(255,255,255,0.12)"
                          : "1px solid rgba(0,0,0,0.09)",
                      backgroundColor:
                        theme === "dark"
                          ? "rgba(255,255,255,0.04)"
                          : "rgba(255,255,255,0.8)",
                      transition: "transform 0.22s ease, border-color 0.22s ease",
                      "&:hover": {
                        transform: "translateY(-6px)",
                        borderColor:
                          theme === "dark"
                            ? "rgba(255,255,255,0.32)"
                            : "rgba(0,0,0,0.18)",
                      },
                    }}
                  >
                    <Stack spacing={1.5}>
                      <Box
                        sx={{
                          width: 52,
                          height: 52,
                          borderRadius: "50%",
                          display: "grid",
                          placeItems: "center",
                          backgroundColor:
                            theme === "dark"
                              ? "rgba(255,107,53,0.2)"
                              : "rgba(43,95,58,0.12)",
                          color: theme === "dark" ? "#FFB08D" : "#2B5F3A",
                        }}
                      >
                        {card.icon}
                      </Box>
                      <Typography
                        sx={{
                          fontFamily: "'Cinzel', serif",
                          fontSize: "1.15rem",
                          fontWeight: 700,
                          color: currentTheme.colors.textPrimary,
                        }}
                      >
                        {card.title}
                      </Typography>
                      <Typography
                        sx={{
                          fontFamily: "'Manrope', sans-serif",
                          lineHeight: 1.65,
                          color: currentTheme.colors.textSecondary,
                        }}
                      >
                        {card.text}
                      </Typography>
                    </Stack>
                  </Paper>
                </Box>
              ))}
            </Box>

            <Box
              data-reveal
              className="reveal-item"
              sx={{
                "--reveal-delay": "140ms",
                mt: { xs: 4, md: 6 },
                mb: { xs: 1, md: 2 },
                p: { xs: 2.2, md: 3 },
                borderRadius: 3,
                border:
                  theme === "dark"
                    ? "1px solid rgba(255,255,255,0.14)"
                    : "1px solid rgba(0,0,0,0.09)",
                background:
                  theme === "dark"
                    ? "linear-gradient(130deg, rgba(255,107,53,0.08), rgba(255,255,255,0.04))"
                    : "linear-gradient(130deg, rgba(43,95,58,0.1), rgba(255,255,255,0.8))",
              }}
            >
              <Typography
                sx={{
                  fontFamily: "'Cinzel', serif",
                  fontSize: { xs: "1.4rem", md: "2rem" },
                  textAlign: "center",
                  mb: 2.2,
                  color: currentTheme.colors.textPrimary,
                }}
              >
                How Your Journey Flows
              </Typography>

              <Box
                sx={{
                  display: "grid",
                  gap: 1.6,
                  gridTemplateColumns: { xs: "1fr", md: "repeat(3, minmax(0, 1fr))" },
                }}
              >
                {steps.map((step, index) => (
                  <Paper
                    key={step.title}
                    elevation={0}
                    className="spotlight-sheen"
                    sx={{
                      p: 2,
                      borderRadius: 2.5,
                      background: theme === "dark" ? "rgba(0,0,0,0.24)" : "rgba(255,255,255,0.82)",
                      border:
                        theme === "dark"
                          ? "1px solid rgba(255,255,255,0.16)"
                          : "1px solid rgba(0,0,0,0.09)",
                    }}
                  >
                    <Stack spacing={1.1}>
                      <Stack direction="row" alignItems="center" spacing={1}>
                        <Box
                          sx={{
                            width: 34,
                            height: 34,
                            borderRadius: "50%",
                            display: "grid",
                            placeItems: "center",
                            background:
                              theme === "dark"
                                ? "rgba(255,107,53,0.2)"
                                : "rgba(43,95,58,0.16)",
                            color: theme === "dark" ? "#FFB08D" : "#2B5F3A",
                          }}
                        >
                          {step.icon}
                        </Box>
                        <Typography
                          sx={{
                            fontFamily: "'Manrope', sans-serif",
                            fontWeight: 800,
                            fontSize: "0.83rem",
                            letterSpacing: "0.08em",
                            opacity: 0.75,
                          }}
                        >
                          STEP {index + 1}
                        </Typography>
                      </Stack>

                      <Typography
                        sx={{
                          fontFamily: "'Cinzel', serif",
                          fontSize: "1.08rem",
                          lineHeight: 1.45,
                          color: currentTheme.colors.textPrimary,
                        }}
                      >
                        {step.title}
                      </Typography>

                      <Typography
                        sx={{
                          fontFamily: "'Manrope', sans-serif",
                          lineHeight: 1.65,
                          color: currentTheme.colors.textSecondary,
                        }}
                      >
                        {step.text}
                      </Typography>
                    </Stack>
                  </Paper>
                ))}
              </Box>
            </Box>

            <Box
              data-reveal
              className="reveal-item"
              sx={{
                "--reveal-delay": "170ms",
                mt: { xs: 4, md: 6 },
                textAlign: "center",
              }}
            >
              <Typography
                sx={{
                  fontFamily: "'Manrope', sans-serif",
                  fontWeight: 800,
                  letterSpacing: "0.12em",
                  fontSize: { xs: "0.78rem", md: "0.85rem" },
                  opacity: 0.7,
                  mb: 1,
                }}
              >
                BUILT FOR REAL ROUTINES
              </Typography>
              <Typography
                sx={{
                  fontFamily: "'Cinzel', serif",
                  fontSize: { xs: "1.65rem", md: "2.55rem" },
                  lineHeight: 1.2,
                  maxWidth: 820,
                  mx: "auto",
                  color: theme === "dark" ? "#F4E6C2" : "#1A1A1A",
                }}
              >
                This Is Not Just Another Diet App.
                <br />
                It Is Your Personal Execution System.
              </Typography>
            </Box>

            <Box
              data-reveal
              className="reveal-item"
              sx={{ textAlign: "center", mt: { xs: 4, md: 5 }, "--reveal-delay": "210ms" }}
            >
              <Button
                variant="contained"
                onClick={() => navigate("/login")}
                sx={{
                  textTransform: "none",
                  px: 4.5,
                  py: 1.35,
                  borderRadius: 999,
                  fontSize: "1rem",
                  fontFamily: "'Cinzel', serif",
                  letterSpacing: "0.03em",
                  backgroundColor: theme === "dark" ? "#FF6B35" : "#2B5F3A",
                  color: "#fff",
                  boxShadow:
                    theme === "dark"
                      ? "0 12px 30px rgba(255,107,53,0.25)"
                      : "0 12px 30px rgba(43,95,58,0.2)",
                  "&:hover": {
                    backgroundColor: theme === "dark" ? "#E85A24" : "#214C2E",
                    transform: "translateY(-2px)",
                  },
                  transition: "all 0.25s ease",
                }}
              >
                Generate Yours
              </Button>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default AppShowcasePage;
