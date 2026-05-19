from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    id: int
    name: str


class UserProfile(UserBase):
    """Схема профиля пользователя"""
    followers: List[UserBase] = []
    following: List[UserBase] = []

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    """Ответ с профилем"""
    result: bool
    user: UserProfile