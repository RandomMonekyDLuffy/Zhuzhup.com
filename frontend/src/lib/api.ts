export type UserRole = "customer" | "professional";

export type Salon = {
  id: number;
  name: string;
  address: string;
  city: string;
  description?: string | null;
};

export type Service = {
  id: number;
  salon_id: number;
  name: string;
  duration_minutes: number;
  price: number;
};

export type BookingType = "scheduled" | "walk_in";

export type BookingCreate = {
  salon_id: number;
  service_id: number;
  professional_id?: number | null;
  booking_type: BookingType;
  scheduled_at?: string | null;
  is_walk_in_now?: boolean;
  notes?: string | null;
};

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    }
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return (await res.json()) as T;
}

export function getToken(): string | null {
  return localStorage.getItem("token");
}

export function setToken(token: string | null) {
  if (!token) localStorage.removeItem("token");
  else localStorage.setItem("token", token);
}

export async function signup(input: {
  email: string;
  full_name: string;
  password: string;
  role: UserRole;
}) {
  return await http<{ id: number; email: string; full_name: string; role: UserRole }>(
    "/auth/signup",
    { method: "POST", body: JSON.stringify(input) }
  );
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Login failed: ${res.status}`);
  }
  return (await res.json()) as { access_token: string; token_type: string };
}

export async function listSalons() {
  return await http<Salon[]>("/salons");
}

export async function listServices(salonId: number) {
  return await http<Service[]>(`/salons/${salonId}/services`);
}

export async function createBooking(input: BookingCreate) {
  const token = getToken();
  if (!token) throw new Error("Not authenticated");
  return await http<any>("/bookings", {
    method: "POST",
    body: JSON.stringify(input),
    headers: { Authorization: `Bearer ${token}` }
  });
}

