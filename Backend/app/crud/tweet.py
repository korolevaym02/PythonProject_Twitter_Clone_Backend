from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.tweet import Tweet, likes_table, tweet_medias_table
from ..models.user import User, follows_table
from typing import List


def create_tweet(
        db: Session,
        content: str,
        media_ids: List[int],
        user_id: int
) -> int:
    tweet = Tweet(content=content, user_id=user_id)
    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    for media_id in media_ids:
        stmt = tweet_medias_table.insert().values(
            tweet_id=tweet.id,
            media_id=media_id
        )
        db.execute(stmt)

    db.commit()
    return tweet.id


def delete_tweet(db: Session, tweet_id: int, user_id: int) -> bool:
    tweet = db.query(Tweet).filter(
        and_(Tweet.id == tweet_id, Tweet.user_id == user_id)
    ).first()

    if not tweet:
        return False

    db.delete(tweet)
    db.commit()
    return True


def like_tweet(db: Session, user_id: int, tweet_id: int) -> bool:
    existing_like = db.query(likes_table).filter(
        and_(likes_table.c.user_id == user_id, likes_table.c.tweet_id == tweet_id)
    ).first()

    if existing_like:
        return False

    stmt = likes_table.insert().values(user_id=user_id, tweet_id=tweet_id)
    try:
        db.execute(stmt)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False


def unlike_tweet(db: Session, user_id: int, tweet_id: int) -> bool:
    stmt = likes_table.delete().where(
        and_(likes_table.c.user_id == user_id, likes_table.c.tweet_id == tweet_id)
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0


def get_user_feed(db: Session, user_id: int, limit: int = 20, offset: int = 0) -> List[Tweet]:
    followed_users_subq = db.query(follows_table.c.followed_id).filter(
        follows_table.c.follower_id == user_id
    ).subquery()

    own_user_subq = db.query(User.id).filter(User.id == user_id).subquery()
    allowed_users = followed_users_subq.union(own_user_subq).subquery()

    tweets = (db.query(Tweet)
              .outerjoin(User, Tweet.user_id == User.id)
              .filter(Tweet.user_id.in_(allowed_users))
              .order_by(Tweet.created_at.desc())
              .limit(limit)
              .offset(offset)
              .all())

    return tweets