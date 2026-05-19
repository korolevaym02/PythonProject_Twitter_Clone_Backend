from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from ..models.user import User, follows_table


def get_user_by_api_key(db: Session, api_key: str) -> Optional[User]:
    """Получить пользователя по API ключу."""
    return db.query(User).filter(User.api_key == api_key).first()


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Получить пользователя по ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """Получить профиль пользователя с подписчиками и подписками"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.followers
        user.following
    return user


def follow_user(db: Session, follower_id: int, followed_id: int) -> bool:
    """Подписаться на пользователя"""
    if follower_id == followed_id:
        return False

    follower = get_user(db, follower_id)
    followed = get_user(db, followed_id)
    if not follower or not followed:
        return False

    try:
        stmt = follows_table.insert().values(
            follower_id=follower_id,
            followed_id=followed_id
        )
        db.execute(stmt)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False


def unfollow_user(db: Session, follower_id: int, followed_id: int) -> bool:
    """Отписаться от пользователя"""
    stmt = follows_table.delete().where(
        and_(
            follows_table.c.follower_id == follower_id,
            follows_table.c.followed_id == followed_id
        )
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0