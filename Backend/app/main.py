from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base, engine
from app.api.v1 import api_router
from app.core.config import settings


# Создаем таблицы при запуске
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Сервис микроблогов API",
    description="Корпоративный сервис микроблогов (ТЗ)",
    version="1.0.0"
)


# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Подключаем API роутер
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Swagger документация доступна на /docs"""
    return {
        "message": "Сервис микроблогов API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}