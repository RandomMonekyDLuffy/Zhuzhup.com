import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="stackLg">
      <section className="hero">
        <div className="stack">
          <h1>Find and book salons in minutes.</h1>
          <p className="muted">
            Browse nearby salons, compare services, and create scheduled or walk‑in bookings.
          </p>
          <div className="row">
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
          <h3>Modular backend</h3>
          <p className="muted">FastAPI routers, schemas, and services for easy scaling.</p>
        </div>
      </section>
    </div>
  );
}

