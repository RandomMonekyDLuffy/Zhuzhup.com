import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Render/Vercel-style env vars are often comma-separated. This makes
    # `cors_origins=a,b,c` parse into ["a", "b", "c"] instead of requiring JSON.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_parse_delimiter=",")

    app_name: str = "Salon Aggregator API"
    # Comma-separated list also supported via env, e.g.
    # cors_origins="http://localhost:5173,https://zhuzhup.com,https://www.zhuzhup.com"
    cors_origins: list[str] = ["http://localhost:5173"]

    sqlite_path: str = "app.db"

    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_minutes: int = 60 * 24

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v):
        # Accept:
        # - JSON list: ["https://a.com","https://b.com"]
        # - Comma-separated: https://a.com,https://b.com
        # - Single string: https://a.com
        if v is None:
            return ["http://localhost:5173"]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return ["http://localhost:5173"]
            if s.startswith("["):
                try:
                    arr = json.loads(s)
                    if isinstance(arr, list):
                        return [str(x).strip() for x in arr if str(x).strip()]
                except Exception:
                    pass
            return [part.strip() for part in s.split(",") if part.strip()]
        return v


settings = Settings()

