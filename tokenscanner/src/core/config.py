import os
import secrets
from typing import Literal, Optional

from pydantic import HttpUrl

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# we have the .env file right in the src folder and not the root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):  # type: ignore
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SERVER_NAME: str = os.getenv("SERVER_NAME", "localhost")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost")

    PROJECT_NAME: str = "Token Scanner"
    PROJECT_VERSION: str = "1.0.0"

    ENVIRONMENT: Literal["local", "production"] = os.getenv("ENVIRONMENT", "local")
    SENTRY_DSN: Optional[HttpUrl] = None

    DATABASE_URI: Optional[str]

    DEBUG_ENABLED: bool = os.getenv("DEBUG_ENABLED", "false").lower() == "true"

    DEXSCREENER_BASE_URI: str = "https://api.dexscreener.com"

    PROJECT_SUMMARY: str = """Scan token liquidity and pool info from DEX Screener
    across chains."""

    PROJECT_DESCRIPTION: str = """
        Token Scanner provides initiutive API to quickly scan tokens and get their
        information such as transaction history, balance, and more. It is designed to be
        ultra-fast, reliable, and easy to use.
        """

    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8")


settings = Settings()  # type: ignore
