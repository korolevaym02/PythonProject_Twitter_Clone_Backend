import pytest
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_api_key, follow_user, create_user


def test_get_user_by_api_key(db_session: Session):
    """Тест получения пользователя по api-key."""
    from app.models.user import User

    user = create_user(db_session, "testuser")
    db_session.commit()

    result = get_user_by_api_key(db_session, user.api_key)
    assert result is not None
    assert result.name == "testuser"

    result = get_user_by_api_key(db_session, "nonexistent")
    assert result is None


def test_follow_user(db_session: Session):
    """Тест фолловинга."""
    user1 = create_user(db_session, "user1")
    user2 = create_user(db_session, "user2")
    db_session.commit()

    result = follow_user(db_session, user1.id, user2.id)
    assert result is True

    result = follow_user(db_session, user1.id, user1.id)
    assert result is False