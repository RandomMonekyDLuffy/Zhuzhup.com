import { Link } from "react-router-dom";
import NearbySearch from "../components/NearbySearch";

export default function LandingPage() {
  return (
    <div className="stackLg">
      <section className="hero">
        <div className="stack">
          <h1>Find and book salons near you.</h1>
          <p className="muted">
            Search services and get professionals in your area. Schedule ahead or walk in.
          </p>

          <NearbySearch />

          <div className="row" style={{ marginTop: 6 }}>
            <Link className="btn" to="/salons">
              Browse salons
            </Link>
            <Link className="btn btnSecondary" to="/auth">
              Login / Signup
            </Link>
          </div>
        </div>
      </section>

      <section className="grid3">
        <div className="card">
          <h3>Salon discovery</h3>
          <p className="muted">Search listings and view services per salon.</p>
        </div>
        <div className="card">
          <h3>Scheduled + walk‑in</h3>
          <p className="muted">Book a time slot, or create a walk‑in request.</p>
        </div>
        <div className="card">
          <h3>Nearby professionals</h3>
          <p className="muted">Auto-detect your location to show services nearby.</p>
        </div>
      </section>
    </div>
  );
}

