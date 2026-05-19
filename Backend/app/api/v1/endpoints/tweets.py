from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.api.deps import get_current_user
from app.crud.tweet import (
    create_tweet, delete_tweet, like_tweet, unlike_tweet, get_user_feed
)
from app.schemas.tweet import TweetResponse, TweetsResponse
from app.models.user import User


router = APIRouter()


@router.post("", response_model=TweetResponse)
async def api_create_tweet(
    tweet_data: str = Form(..., description="Текст твита (макс. 280 символов)"),
    tweet_media_ids: List[int] = Form(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новый твит"""
    if len(tweet_data) > 280:
        raise HTTPException(400, "Tweet too long")

    if not tweet_data.strip() and not tweet_media_ids:
        raise HTTPException(400, "Tweet must have content or media")

    tweet_id = create_tweet(db, tweet_data, tweet_media_ids, current_user.id)
    return TweetResponse(result=True, tweet_id=tweet_id)


@router.delete("/{tweet_id}", response_model=dict)
async def api_delete_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить свой твит"""
    if not delete_tweet(db, tweet_id, current_user.id):
        raise HTTPException(status_code=404, detail="Tweet not found or not yours")
    return {"result": True}


@router.get("", response_model=TweetsResponse)
async def api_get_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить ленту"""
    tweets = get_user_feed(db, current_user.id)
    return TweetsResponse(result=True, tweets=tweets)


@router.post("/{tweet_id}/likes", response_model=dict)
async def api_like_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Поставить лайк"""
    if like_tweet(db, current_user.id, tweet_id):
        return {"result": True}
    raise HTTPException(400, "Already liked or tweet not found")


@router.delete("/{tweet_id}/likes", response_model=dict)
async def api_unlike_tweet(
    tweet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Убрать лайк"""
    if unlike_tweet(db, current_user.id, tweet_id):
        return {"result": True}
    raise HTTPException(400, "Not liked or tweet not found")