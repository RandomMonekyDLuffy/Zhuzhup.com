import { Navigate, Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import AuthPage from "./pages/AuthPage";
import SalonListPage from "./pages/SalonListPage";
import BookingPage from "./pages/BookingPage";
import { TopNav } from "./components/TopNav";

export default function App() {
  return (
    <div className="appShell">
      <TopNav />
      <main className="container">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/salons" element={<SalonListPage />} />
          <Route path="/book" element={<BookingPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

