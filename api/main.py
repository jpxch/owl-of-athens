from fastapi import FastAPI
from app.core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/health", tags=["system"])
    def health_check():
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "environment": settings.ENVIRONMENT,
        }

    return app

app = create_application()