import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { NotificationProvider } from "./context/NotificationContext";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import UserDetailsPage from "./pages/UserDetailsPage";
import PlanResultPage from "./pages/PlanResultPage";
import AppShowcasePage from "./pages/AppShowcasePage";
import ThemeToggle from "./components/ThemeToggle";
import NotificationCenter from "./components/NotificationCenter";
import { Box } from "@mui/material";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <NotificationProvider>
          <Box
            sx={{
              position: "fixed",
              top: "calc(env(safe-area-inset-top, 0px) + 10px)",
              left: "calc(env(safe-area-inset-left, 0px) + 10px)",
              zIndex: 1400,
            }}
          >
            <ThemeToggle />
          </Box>
          <Box
            sx={{
              position: "fixed",
              top: "calc(env(safe-area-inset-top, 0px) + 10px)",
              right: "calc(env(safe-area-inset-right, 0px) + 10px)",
              zIndex: 1400,
            }}
          >
            <NotificationCenter />
          </Box>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/about" element={<AppShowcasePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/details" element={<UserDetailsPage />} />
            <Route path="/result" element={<PlanResultPage />} />
          </Routes>
        </NotificationProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;

