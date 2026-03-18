import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Salon Aggregator API"
    # Keep as a string in env to avoid Render/pydantic list parsing issues.
    # Accepts either:
    # - comma-separated: https://a.com,https://b.com
    # - JSON list: ["https://a.com","https://b.com"]
    cors_origins: str = "http://localhost:5173"

    sqlite_path: str = "app.db"

    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_minutes: int = 60 * 24

    @property
    def cors_origins_list(self) -> list[str]:
        raw = (self.cors_origins or "").strip()
        if not raw:
            return ["http://localhost:5173"]
        if raw.startswith("["):
            try:
                arr = json.loads(raw)
                if isinstance(arr, list):
                    vals = [str(x).strip() for x in arr if str(x).strip()]
                    return vals or ["http://localhost:5173"]
            except Exception:
                pass
        vals = [p.strip() for p in raw.split(",") if p.strip()]
        return vals or ["http://localhost:5173"]


settings = Settings()

