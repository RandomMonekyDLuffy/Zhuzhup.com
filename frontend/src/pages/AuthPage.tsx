import { FormEvent, useMemo, useState } from "react";
import { login, setToken, signup, type UserRole } from "../lib/api";
import { useNavigate } from "react-router-dom";

export default function AuthPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("customer");
  const [status, setStatus] = useState<string | null>(null);

  const canSubmit = useMemo(() => {
    if (!email || !password) return false;
    if (mode === "signup" && !fullName) return false;
    return true;
  }, [email, password, fullName, mode]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus(null);
    try {
      if (mode === "signup") {
        await signup({ email, full_name: fullName, password, role });
      }
      const tok = await login(email, password);
      setToken(tok.access_token);
      navigate("/salons");
    } catch (err: any) {
      setStatus(err?.message ?? "Something went wrong");
    }
  }

  return (
    <div className="stackLg">
      <h2>{mode === "login" ? "Login" : "Signup"}</h2>

      <div className="row">
        <button
          className={mode === "login" ? "pill pillActive" : "pill"}
          onClick={() => setMode("login")}
          type="button"
        >
          Login
        </button>
        <button
          className={mode === "signup" ? "pill pillActive" : "pill"}
          onClick={() => setMode("signup")}
          type="button"
        >
          Signup
        </button>
      </div>

      <form className="card stack" onSubmit={onSubmit}>
        <label className="field">
          <span>Email</span>
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>

        {mode === "signup" ? (
          <>
            <label className="field">
              <span>Full name</span>
              <input value={fullName} onChange={(e) => setFullName(e.target.value)} required />
            </label>
            <label className="field">
              <span>Role</span>
              <select value={role} onChange={(e) => setRole(e.target.value as UserRole)}>
                <option value="customer">Customer</option>
                <option value="professional">Professional</option>
              </select>
            </label>
          </>
        ) : null}

        <label className="field">
          <span>Password</span>
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            minLength={8}
          />
        </label>

        {status ? <div className="error">{status}</div> : null}

        <button className="btn" disabled={!canSubmit}>
          {mode === "login" ? "Login" : "Create account"}
        </button>
      </form>
    </div>
  );
}

