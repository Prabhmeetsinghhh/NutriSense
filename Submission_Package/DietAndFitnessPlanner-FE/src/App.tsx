import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import UserDetailsPage from "./pages/UserDetailsPage";
import PlanResultPage from "./pages/PlanResultPage";
import AppShowcasePage from "./pages/AppShowcasePage";
import ThemeToggle from "./components/ThemeToggle";
import { Box } from "@mui/material";

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
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
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<AppShowcasePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/details" element={<UserDetailsPage />} />
          <Route path="/result" element={<PlanResultPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;

