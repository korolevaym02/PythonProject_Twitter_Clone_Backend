import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db
from app.core.config import settings


SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    """Тестовый engine."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL_TEST,
        connect_args={"check_same_thread": False}
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Тестовая БД сессия"""
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def override_get_db(db_session):
    """Переопределяем get_db dependency"""

    async def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    return _override_get_db


@pytest.fixture
def client(override_get_db):
    """FastAPI TestClient с моками"""
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
def create_test_users(db_session):
    """Создает тестовых пользователей."""
    from app.models.user import User
    from app.crud.user import generate_api_key

    user1 = User(name="testuser1", api_key="test-api-key-1")
    user2 = User(name="testuser2", api_key="test-api-key-2")

    db_session.add_all([user1, user2])
    db_session.commit()

    return {
        "user1": {"id": user1.id, "api_key": user1.api_key},
        "user2": {"id": user2.id, "api_key": user2.api_key}
    }