"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    mongodb_url: str = Field(
        ...,
        description="MongoDB connection string",
    )

    mongodb_database: str = Field(
        ...,
        description="MongoDB database name",
    )

    api_key_hash: str = Field(
        ...,
        description="SHA-256 hash of the API key",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()