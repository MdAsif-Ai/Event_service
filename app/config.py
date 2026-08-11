
"""Application configuration using pydantic-settings.

All values are read from environment variables, making it safe to store
secrets outside of source control. The Settings class can be instantiated
once at application startup and injected wherever needed.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration values required by the Event Service."""

    mongodb_url: str = Field(..., env="MONGODB_URL", description="MongoDB connection string")
    mongodb_database: str = Field(..., env="MONGODB_DATABASE", description="MongoDB database name")
    api_key_hash: str = Field(..., env="API_KEY_HASH", description="SHA-256 hash of the API key")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

# Export a singleton instance for easy import across the project.
settings = Settings()
