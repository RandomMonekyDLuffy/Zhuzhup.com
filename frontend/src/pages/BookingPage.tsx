import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  createBooking,
  getToken,
  listSalons,
  listServices,
  type BookingType,
  type Salon,
  type Service
} from "../lib/api";

function isoNowPlusHours(hours: number) {
  const d = new Date(Date.now() + hours * 60 * 60 * 1000);
  return d.toISOString();
}

export default function BookingPage() {
  const nav = useNavigate();
  const [params] = useSearchParams();

  const [salons, setSalons] = useState<Salon[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [salonId, setSalonId] = useState<number | null>(null);
  const [serviceId, setServiceId] = useState<number | null>(null);
  const [bookingType, setBookingType] = useState<BookingType>("scheduled");
  const [scheduledAt, setScheduledAt] = useState<string>(isoNowPlusHours(2));
  const [notes, setNotes] = useState<string>("");
  const [status, setStatus] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const fromQuery = params.get("salonId");
    if (fromQuery) setSalonId(Number(fromQuery));
  }, [params]);

  useEffect(() => {
    (async () => {
      try {
        const s = await listSalons();
        setSalons(s);
      } catch (e: any) {
        setStatus(e?.message ?? "Failed to load salons");
      }
    })();
  }, []);

  useEffect(() => {
    if (!salonId) return;
    (async () => {
      try {
        const svc = await listServices(salonId);
        setServices(svc);
        setServiceId(svc[0]?.id ?? null);
      } catch (e: any) {
        setStatus(e?.message ?? "Failed to load services");
      }
    })();
  }, [salonId]);

  const needsAuth = !getToken();

  const canSubmit = useMemo(() => {
    if (needsAuth) return false;
    if (!salonId || !serviceId) return false;
    if (bookingType === "scheduled" && !scheduledAt) return false;
    return true;
  }, [needsAuth, salonId, serviceId, bookingType, scheduledAt]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus(null);
    setBusy(true);
    try {
      const payload = {
        salon_id: salonId!,
        service_id: serviceId!,
        booking_type: bookingType,
        scheduled_at: bookingType === "scheduled" ? scheduledAt : null,
        is_walk_in_now: bookingType === "walk_in",
        notes: notes || null
      };
      await createBooking(payload);
      setStatus("Booking created.");
      setTimeout(() => nav("/salons"), 700);
    } catch (e: any) {
      setStatus(e?.message ?? "Failed to create booking");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="stackLg">
      <h2>Create booking</h2>

      {needsAuth ? (
        <div className="card stack">
          <div className="error">You must login first to create a booking.</div>
          <button className="btn" onClick={() => nav("/auth")} type="button">
            Go to Login / Signup
          </button>
        </div>
      ) : null}

      <form className="card stack" onSubmit={onSubmit}>
        <label className="field">
          <span>Salon</span>
          <select
            value={salonId ?? ""}
            onChange={(e) => setSalonId(Number(e.target.value))}
            required
          >
            <option value="" disabled>
              Select a salon
            </option>
            {salons.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} — {s.city}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Service</span>
          <select
            value={serviceId ?? ""}
            onChange={(e) => setServiceId(Number(e.target.value))}
            required
            disabled={!salonId}
          >
            {services.length === 0 ? (
              <option value="" disabled>
                Select a salon first
              </option>
            ) : null}
            {services.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.duration_minutes}m) — ${s.price.toFixed(2)}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Booking type</span>
          <select value={bookingType} onChange={(e) => setBookingType(e.target.value as BookingType)}>
            <option value="scheduled">Scheduled</option>
            <option value="walk_in">Walk-in</option>
          </select>
        </label>

        {bookingType === "scheduled" ? (
          <label className="field">
            <span>Scheduled at (ISO)</span>
            <input value={scheduledAt} onChange={(e) => setScheduledAt(e.target.value)} />
            <span className="hint">Example: 2026-03-18T10:00:00Z</span>
          </label>
        ) : (
          <div className="muted">Walk-in creates a booking without a time slot.</div>
        )}

        <label className="field">
          <span>Notes (optional)</span>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={3} />
        </label>

        {status ? <div className={status.includes("created") ? "ok" : "error"}>{status}</div> : null}

        <button className="btn" disabled={!canSubmit || busy}>
          {busy ? "Creating..." : "Create booking"}
        </button>
      </form>
    </div>
  );
}

