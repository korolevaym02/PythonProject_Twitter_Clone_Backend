from pydantic import BaseModel
from typing import List
from .user import UserBase


class Tweet(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: UserBase
    likes: List[UserBase] = []


class TweetResponse(BaseModel):
    result: bool
    tweet_id: int


class TweetsResponse(BaseModel):
    result: bool
    tweets: List[Tweet]


class ApiError(BaseModel):
    """Схема ошибки"""
    result: bool = False
    error_type: str
    error_message: str
