from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "postgresql://twitter:twitterpass@db:5432/twitter"
    DATABASE_URL_LOCAL: Optional[str] = "sqlite:///./twitter.db"

    # API
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    API_V1_STR: str = "/api"

    # Лимиты
    MAX_TWEET_LENGTH: int = 280
    MAX_MEDIA_SIZE: int = 10 * 1024 * 1024

    # Медиа
    MEDIA_PATH: str = "./media"
    MEDIA_URL_PATH: str = "/media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


# Автовыбор БД (локально SQLite, Docker PostgreSQL)
if settings.DATABASE_URL_LOCAL and not os.getenv("DOCKER_ENV"):
    settings.DATABASE_URL = settings.DATABASE_URL_LOCAL