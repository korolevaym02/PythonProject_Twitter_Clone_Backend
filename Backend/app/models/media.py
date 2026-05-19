from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())