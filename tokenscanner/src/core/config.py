import os
import secrets
from typing import Literal

from pydantic import AnyHttpUrl, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SERVER_NAME: str = os.getenv("SERVER_NAME", "localhost")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost")

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Token Scanner")
    PROJECT_VERSION: str = "0.1.0"

    CORS_ALLOWED_ORIGINS: list[AnyHttpUrl] = os.getenv("CORS_ALLOWED_ORIGINS", [])

    ENVIRONMENT: Literal["local", "production"] = os.getenv("ENVIRONMENT", "local")
    SENTRY_DSN: HttpUrl | None = None

    DATABASE_URI: str | None = None

    DEBUG_ENABLED: bool = os.getenv("DEBUG_ENABLED", "false").lower() == "true"

    DEXSCREENER_BASE_URI: str = "https://api.dexscreener.com"

    PROJECT_SUMMARY: str = """Scan token liquidity and pool info from DEX Screener
    across chains."""

    PROJECT_DESCRIPTION: str = """
        Token Scanner provides initiutive API to quickly scan tokens and get their
        information such as transaction history, balance, and more. It is designed to be
        ultra-fast, reliable, and easy to use.
        """


settings = Settings()  # type: ignore
