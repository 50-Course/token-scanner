import sentry_sdk
from fastapi import FastAPI
from src.core.config import settings
from src.api.routes import router as api_router

app = FastAPI(
    debug=settings.DEBUG_ENABLED if settings.DEBUG_ENABLED else False,
    title=settings.PROJECT_NAME,
    summary=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

if settings.CORS_ALLOWED_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
