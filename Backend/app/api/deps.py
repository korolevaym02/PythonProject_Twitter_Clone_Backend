from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..crud.user import get_user_by_api_key
from ..db.session import get_db
from ..models.user import User


async def get_current_user(
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db)
) -> User:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing api-key header"
        )

    user = get_user_by_api_key(db, api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid api-key"
        )

    return user