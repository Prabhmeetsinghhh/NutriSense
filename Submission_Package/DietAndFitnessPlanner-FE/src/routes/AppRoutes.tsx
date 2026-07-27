import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "../pages/LandingPage";
import LoginPage from "../pages/LoginPage";
import UserDetailsPage from "../pages/UserDetailsPage";
import PlanResultPage from "../pages/PlanResultPage";

const AppRoutes = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/details" element={<UserDetailsPage />} />
      <Route path="/result" element={<PlanResultPage />} />
    </Routes>
  </BrowserRouter>
);

export default AppRoutes;

