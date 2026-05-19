from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


likes_table = Table(
    "likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
    PrimaryKeyConstraint("user_id", "tweet_id")
)


tweet_medias_table = Table(
    "tweet_medias",
    Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
    Column("media_id", Integer, ForeignKey("medias.id")),
    PrimaryKeyConstraint("tweet_id", "media_id")
)


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(280), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="tweets")
    likes = relationship("User", secondary=likes_table)
    medias = relationship("Media", secondary=tweet_medias_table)