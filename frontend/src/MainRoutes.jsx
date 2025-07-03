import { BrowserRouter, Routes, Route } from "react-router-dom";
import DecksPage from "./pages/DecksPage";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import StudyPage from "./pages/StudyPage";
import DeckPage from "./pages/DeckPage";
import RegisterPage from "./pages/RegisterPage";
import SettingsPage from "./pages/SettingsPage";
import VerificationPage from "./pages/VerificationPage";

export function MainRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/decks" element={<DecksPage />} />
        <Route path="/decks/:deck_id" element={<DeckPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/study" element={<StudyPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verification" element={<VerificationPage />} />
      </Routes>
    </BrowserRouter>
  );
}
