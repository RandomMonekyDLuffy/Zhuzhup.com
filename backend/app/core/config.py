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


settings = Settings()

