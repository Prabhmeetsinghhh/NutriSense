import { Box, Typography, Button, Container, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { getTheme } from "../theme/indianTheme";

const LandingPage = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const currentTheme = getTheme(theme);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        background:
          theme === "dark"
            ? "radial-gradient(circle at 15% 12%, rgba(212,175,55,0.14), rgba(212,175,55,0) 36%), linear-gradient(120deg, #09090b 0%, #14121b 60%, #15120f 100%)"
            : "radial-gradient(circle at 15% 10%, rgba(43,95,58,0.12), rgba(43,95,58,0) 36%), linear-gradient(120deg, #F5F1E8 0%, #FAFAF8 60%, #F8F6F1 100%)",
        color: currentTheme.colors.textPrimary,
        fontFamily: "'Cormorant Garamond', 'Times New Roman', serif",
        display: "flex",
        alignItems: "center",
        py: { xs: 2, md: 5 },
        transition: "background-color 0.3s ease",
      }}
    >
      <style>
        {`@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');`}
      </style>

      <Container
        maxWidth="xl"
        sx={{
          px: { xs: 1.5, md: 3 },
        }}
      >
        <Box
          sx={{
            maxWidth: 1220,
            mx: "auto",
            borderRadius: 2,
            border:
              theme === "dark"
                ? "1px solid rgba(255, 255, 255, 0.18)"
                : "1px solid rgba(0, 0, 0, 0.1)",
            background:
              theme === "dark"
                ? "linear-gradient(90deg, rgba(22,18,30,0.95) 0%, rgba(14,14,18,0.96) 100%)"
                : "linear-gradient(90deg, rgba(255,255,255,0.98) 0%, rgba(250,250,248,0.96) 100%)",
            overflow: "hidden",
            boxShadow: currentTheme.shadows.medium,
            backdropFilter: "blur(8px)",
            transition: "all 0.3s ease",
          }}
        >
          <Box
            sx={{
              px: { xs: 2, md: 4 },
              py: { xs: 3, md: 5 },
              display: "grid",
              gridTemplateColumns: { xs: "1fr", md: "0.95fr 1.05fr" },
              gap: { xs: 2.5, md: 3.5 },
              alignItems: "center",
            }}
          >
            <Box
              sx={{
                position: "relative",
                minHeight: { xs: 320, md: 460 },
                borderRadius: 2.5,
                overflow: "hidden",
                border:
                  theme === "dark"
                    ? "1px solid rgba(255,255,255,0.14)"
                    : "1px solid rgba(0,0,0,0.08)",
                backgroundColor:
                  theme === "dark"
                    ? "rgba(0,0,0,0.35)"
                    : "rgba(255,255,255,0.5)",
              }}
            >
              <Box
                component="img"
                src="/images/arnold.jpg"
                alt="Arnold"
                sx={{
                  position: "relative",
                  zIndex: 2,
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  objectPosition: "58% 18%",
                  transform: "scale(1.16) translateX(5%) translateY(-2%)",
                  transformOrigin: "center",
                  filter: "contrast(1.05)",
                }}
              />
            </Box>

            <Box
              sx={{
                textAlign: { xs: "center", md: "left" },
                py: { md: 1 },
                maxWidth: { md: 540 },
                mx: { xs: "auto", md: 0 },
              }}
            >
              <Typography
                sx={{
                  fontFamily: "'Cinzel', serif",
                  fontSize: { xs: "2.4rem", md: "4rem" },
                  lineHeight: 1.1,
                  fontWeight: 800,
                  letterSpacing: "0.04em",
                  color: theme === "dark" ? "#D4AF37" : "#1A1A1A",
                  textShadow:
                    theme === "dark"
                      ? "0 2px 18px rgba(212, 175, 55, 0.24)"
                      : "0 2px 18px rgba(43, 95, 58, 0.08)",
                  mb: 1.25,
                  transition: "color 0.3s ease",
                }}
              >
                {theme === "dark" ? (
                  "NutriSense"
                ) : (
                  <>
                    <Box component="span" sx={{ color: "#2B5F3A" }}>
                      Nutri
                    </Box>
                    <Box component="span" sx={{ color: "#1A1A1A" }}>
                      Sense
                    </Box>
                  </>
                )}
              </Typography>

              <Typography
                sx={{
                  fontFamily: "'Cormorant Garamond', serif",
                  fontSize: { xs: "1.15rem", md: "1.7rem" },
                  lineHeight: 1.35,
                  fontWeight: 500,
                  mb: 3.2,
                  color: currentTheme.colors.textSecondary,
                }}
              >
                Your Body, Your Budget, Your Goals
              </Typography>

              <Stack
                direction={{ xs: "column", sm: "row" }}
                spacing={1.5}
                justifyContent={{ xs: "center", md: "flex-start" }}
              >
                <Button
                  variant="contained"
                  onClick={() => navigate("/login")}
                  sx={{
                    textTransform: "none",
                    px: 3,
                    py: 1.1,
                    minWidth: 148,
                    borderRadius: 999,
                    fontFamily: "'Cinzel', serif",
                    letterSpacing: "0.02em",
                    backgroundColor: theme === "dark" ? "#FF6B35" : "#2B5F3A",
                    color: "#fff",
                    boxShadow:
                      theme === "dark"
                        ? "0 10px 28px rgba(255,107,53,0.24)"
                        : "0 10px 28px rgba(43,95,58,0.2)",
                    "&:hover": {
                      backgroundColor: theme === "dark" ? "#E85A24" : "#214C2E",
                      transform: "translateY(-2px)",
                    },
                    transition: "all 0.3s ease",
                  }}
                >
                  Get Started
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => navigate("/about")}
                  sx={{
                    textTransform: "none",
                    px: 3,
                    py: 1.1,
                    minWidth: 148,
                    borderRadius: 999,
                    fontFamily: "'Cinzel', serif",
                    letterSpacing: "0.02em",
                    color: theme === "dark" ? "#fff" : "#1A1A1A",
                    borderColor:
                      theme === "dark"
                        ? "rgba(255,255,255,0.6)"
                        : "rgba(0,0,0,0.2)",
                    backgroundColor:
                      theme === "dark"
                        ? "transparent"
                        : "rgba(255,255,255,0.5)",
                    "&:hover": {
                      borderColor:
                        theme === "dark"
                          ? "rgba(255,255,255,0.8)"
                          : "rgba(0,0,0,0.4)",
                      backgroundColor:
                        theme === "dark"
                          ? "rgba(255,255,255,0.1)"
                          : "rgba(255,255,255,0.7)",
                      transform: "translateY(-2px)",
                    },
                    transition: "all 0.3s ease",
                  }}
                >
                  Learn More
                </Button>
              </Stack>
            </Box>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default LandingPage;

