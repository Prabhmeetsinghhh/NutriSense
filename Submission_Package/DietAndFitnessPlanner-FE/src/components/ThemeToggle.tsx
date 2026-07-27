import { IconButton, Tooltip } from "@mui/material";
import { DarkMode, LightMode } from "@mui/icons-material";
import { useTheme } from "../context/ThemeContext";

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <Tooltip title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}>
      <IconButton
        onClick={toggleTheme}
        sx={{
          color: theme === "dark" ? "#FFD700" : "#2B5F3A",
          backgroundColor: theme === "dark" ? "rgba(255, 215, 0, 0.12)" : "rgba(43, 95, 58, 0.12)",
          border: theme === "dark" ? "1px solid rgba(255,215,0,0.35)" : "1px solid rgba(43,95,58,0.25)",
          backdropFilter: "blur(6px)",
          boxShadow:
            theme === "dark"
              ? "0 8px 20px rgba(255, 215, 0, 0.18)"
              : "0 8px 20px rgba(43, 95, 58, 0.15)",
          borderRadius: "50%",
          width: 48,
          height: 48,
          transition: "all 0.3s ease",
          "&:hover": {
            backgroundColor: theme === "dark" ? "rgba(255, 215, 0, 0.2)" : "rgba(43, 95, 58, 0.2)",
            transform: "scale(1.06) translateY(-1px)",
          },
        }}
      >
        {theme === "dark" ? (
          <LightMode fontSize="medium" />
        ) : (
          <DarkMode fontSize="medium" />
        )}
      </IconButton>
    </Tooltip>
  );
};

export default ThemeToggle;

