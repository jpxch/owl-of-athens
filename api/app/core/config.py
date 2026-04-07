from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "owl-of-athens"
    ENVIRONMENT: str = "development"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8010
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    DATABASE_URL: str

    MODEL_PROVIDER: str = "openai"

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1"

    ATLAS_BASE_URL: str | None = None
    OLLAMA_BASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
