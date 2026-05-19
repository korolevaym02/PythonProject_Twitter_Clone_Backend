from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_user
from app.crud.user import get_user_profile, follow_user, unfollow_user
from app.schemas.user import ProfileResponse
from app.models.user import User


router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def api_get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Информация о своем профиле"""
    profile = get_user_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(result=True, user=profile)


@router.get("/{user_id}", response_model=ProfileResponse)
async def api_get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Информация о профиле пользователя"""
    profile = get_user_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return ProfileResponse(result=True, user=profile)


@router.post("/{user_id}/follow", response_model=dict)
async def api_follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Зафолловить пользователя"""
    if follow_user(db, current_user.id, user_id):
        return {"result": True}
    raise HTTPException(400, "Already following or invalid user")


@router.delete("/{user_id}/follow", response_model=dict)
async def api_unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отписаться от пользователя"""
    if unfollow_user(db, current_user.id, user_id):
        return {"result": True}
    raise HTTPException(400, "Not following this user")