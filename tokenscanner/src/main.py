import sentry_sdk
from fastapi import FastAPI
from src.core.config import settings
from src.api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    debug=settings.DEBUG_ENABLED if settings.DEBUG_ENABLED else False,
    title=settings.PROJECT_NAME,
    redoc_url="/api/docs",
    docs_url="/",
    # servers=[
    #     {
    #         "url": "http://104.154.104.188:8000",
    #         "description": settings.ENVIRONMENT,
    #     },
    # ],
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/50-Course/token-scanner/blob/main/LICENSE",
    },
    contact={
        "name": "Eri A. (50-Course)",
        "url": "https://github.com/50-Course",
        "email": "eridotdev@proton.me",
    },
    summary=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
