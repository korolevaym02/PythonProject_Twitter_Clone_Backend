from sqlalchemy.orm import Session
from app.models.media import Media
from app.db.base import Base


def create_media(db: Session, file_path: str) -> int:
    """Создать запись о медиафайле"""
    media = Media(file_path=file_path)
    db.add(media)
    db.commit()
    db.refresh(media)
    return media.id