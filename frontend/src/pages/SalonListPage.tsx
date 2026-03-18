import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listSalons, type Salon } from "../lib/api";

export default function SalonListPage() {
  const [items, setItems] = useState<Salon[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await listSalons();
        if (!cancelled) setItems(data);
      } catch (e: any) {
        if (!cancelled) setError(e?.message ?? "Failed to load salons");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="stackLg">
      <div className="row rowBetween">
        <h2>Salons</h2>
        <Link className="btn btnSecondary" to="/book">
          Create booking
        </Link>
      </div>

      {loading ? <div className="muted">Loading...</div> : null}
      {error ? <div className="error">{error}</div> : null}

      <div className="grid2">
        {items.map((s) => (
          <div key={s.id} className="card stack">
            <div className="row rowBetween">
              <h3 style={{ margin: 0 }}>{s.name}</h3>
              <span className="tag">{s.city}</span>
            </div>
            <div className="muted">{s.address}</div>
            {s.description ? <div>{s.description}</div> : null}
            <div className="row">
              <Link className="btn btnSmall" to={`/book?salonId=${s.id}`}>
                Book here
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

