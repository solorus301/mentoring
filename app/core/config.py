from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

settings = Settings()