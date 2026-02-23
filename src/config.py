"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Allow extra env vars in .env without error
    )

    # Application
    app_name: str = "Antigravity Workspace"
    app_version: str = "1.0.0"
    environment: str = Field("development", validation_alias="APP_ENV")
    debug: bool = Field(False, validation_alias="APP_DEBUG")

    # Paths (F-06: Robust relative paths)
    # Allows identifying root regardless of execution dir
    workspace_root: str = "."  # Can be derived using pathlib in future iteration

    # Server
    host: str = "0.0.0.0"
    port: int = Field(8000, validation_alias="APP_PORT")

    # Security
    api_key: str = Field(..., validation_alias="API_KEY")
    frontend_url: str = Field("http://localhost:3000", validation_alias="FRONTEND_URL")

    # Database (optional)
    database_url: str = "sqlite:///./data/app.db"

    # Data Source (Organized Drive)
    data_dir: str = Field(
        r"H:\_UGCO_Disco G_PC_Jefatura\_Organized_2026\02_Administrativo",
        validation_alias="DATA_DIR",
    )

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
