from sqlalchemy import Column, Integer, String, Table, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
import secrets


follows_table = Table(
    "follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id")),
    PrimaryKeyConstraint("follower_id", "followed_id")
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    api_key = Column(String(64), unique=True, index=True, nullable=False)

    tweets = relationship("Tweet", back_populates="user")

    followers = relationship(
        "User",
        secondary=follows_table,
        primaryjoin=(follows_table.c.followed_id == id),
        secondaryjoin=(follows_table.c.follower_id == id),
        back_populates="following"
    )
    following = relationship(
        "User",
        secondary=follows_table,
        primaryjoin=(follows_table.c.follower_id == id),
        secondaryjoin=(follows_table.c.followed_id == id),
        back_populates="followers"
    )


def generate_api_key() -> str:
    """Генерирует безопасный API ключ."""
    return secrets.token_urlsafe(32)