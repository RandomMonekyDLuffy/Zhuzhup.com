import { Link, NavLink, useNavigate } from "react-router-dom";
import { getToken, setToken } from "../lib/api";

export function TopNav() {
  const token = getToken();
  const navigate = useNavigate();

  return (
    <header className="topNav">
      <div className="container topNavInner">
        <Link className="brand" to="/">
          ZhuzhUP
        </Link>
        <nav className="navLinks">
          <NavLink to="/salons">Salons</NavLink>
          <NavLink to="/book">Book</NavLink>
          {!token ? (
            <NavLink to="/auth">Login / Signup</NavLink>
          ) : (
            <button
              className="linkButton"
              onClick={() => {
                setToken(null);
                navigate("/");
              }}
            >
              Logout
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}

