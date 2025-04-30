import os
import secrets
from typing import Literal, Optional, Annotated, Any

from pydantic import HttpUrl, AnyUrl, BeforeValidator, computed_field

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# we have the .env file right in the src folder and not the root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):  # type: ignore
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SERVER_NAME: str = os.getenv("SERVER_NAME", "localhost")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost")

    PROJECT_NAME: str = "Token Scanner"
    PROJECT_VERSION: str = "1.0.0"

    # CORS_ALLOWED_ORIGINS: list[str] = ["*"]
    CORS_ALLOWED_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ALLOWED_ORIGINS]

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
