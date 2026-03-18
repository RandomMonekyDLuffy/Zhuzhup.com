import { FormEvent, useState } from "react";
import { searchProfessionals, type ProfessionalSearchResult } from "../lib/api";

export default function NearbySearch() {
  const [service, setService] = useState("");
  const [location, setLocation] = useState("");
  const [results, setResults] = useState<ProfessionalSearchResult[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [searching, setSearching] = useState(false);
  const [detecting, setDetecting] = useState(false);

  async function runSearch(input: { location?: string | null; lat?: number | null; lng?: number | null }) {
    setError(null);
    setSearching(true);
    try {
      const resp = await searchProfessionals({
        service,
        location: input.location ?? undefined,
        lat: input.lat ?? undefined,
        lng: input.lng ?? undefined
      });
      if (resp.location_used) setLocation(resp.location_used);
      setResults(resp.results);
    } catch (e: any) {
      setError(e?.message ?? "Search failed");
      setResults(null);
    } finally {
      setSearching(false);
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!service.trim()) {
      setError("Please type a service name (e.g. Haircut).");
      return;
    }
    const loc = location.trim() || null;
    void runSearch({ location: loc });
  }

  function onAutoDetect() {
    setError(null);
    if (!service.trim()) {
      setError("Please type a service name first.");
      return;
    }
    if (!navigator.geolocation) {
      setError("Geolocation is not supported in this browser.");
      return;
    }

    setDetecting(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        void (async () => {
          try {
            const resp = await searchProfessionals({
              service,
              lat: pos.coords.latitude,
              lng: pos.coords.longitude
            });
            if (resp.location_used) setLocation(resp.location_used);
            setResults(resp.results);
          } catch (e: any) {
            setError(e?.message ?? "Auto-detect search failed");
            setResults(null);
          } finally {
            setDetecting(false);
          }
        })();
      },
      () => {
        setError("Could not detect your location. Please type your city instead.");
        setDetecting(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }

  return (
    <div className="circleSearchArea">
      <form className="circleSearch" onSubmit={onSubmit}>
        <div className="circleSearchTitle">Search near you</div>

        <label className="circleField">
          <span>Service</span>
          <input
            value={service}
            onChange={(e) => setService(e.target.value)}
            placeholder="Haircut, Blow Dry..."
            required
          />
        </label>

        <label className="circleField">
          <span>Location (city)</span>
          <input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. New York"
          />
        </label>

        <div className="circleActions">
          <button className="btn" type="submit" disabled={searching}>
            {searching ? "Searching..." : "Search"}
          </button>
          <button className="btn btnSecondary" type="button" onClick={onAutoDetect} disabled={detecting}>
            {detecting ? "Detecting..." : "Use my location"}
          </button>
        </div>
      </form>

      {error ? <div className="error circleError">{error}</div> : null}

      {results && results.length > 0 ? (
        <div className="searchResults">
          {results.map((p) => (
            <div key={p.professional_id} className="card resultCard">
              <div className="row rowBetween">
                <h3 style={{ margin: 0 }}>{p.professional_name}</h3>
                <span className="tag">{p.city}</span>
              </div>
              {p.title ? <div className="muted">{p.title}</div> : null}
              <div className="muted">{p.salon_name}</div>
              <div className="searchServices">
                {p.services.map((s) => (
                  <div key={s.id} className="servicePill">
                    {s.name} ({s.duration_minutes}m) - ${s.price.toFixed(2)}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : null}

      {results && results.length === 0 ? <div className="muted">No professionals found.</div> : null}
    </div>
  );
}

