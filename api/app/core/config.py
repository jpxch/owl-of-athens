from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "owl-of-athens"
    ENVIRONMENT: str = "development"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8010

    DATABASE_URL: str

    MODEL_PROVIDER: str = "opneai"

    OPEN_AI_KEY: str | None = None

    ATLAS_BASE_URL: str | None = None
    OLLAMA_BASE_URL: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()