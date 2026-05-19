from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os
import uuid
from app.core.config import settings
from app.db.base import get_db
from app.api.deps import get_current_user
from app.crud.media import create_media
from app.models.user import User
from app.schemas.media import MediaResponse


router = APIRouter()


@router.post("", response_model=dict)
async def api_upload_media(
        file: UploadFile = File(..., description="Изображение"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Загрузить медиафайл для твита"""
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(400, "Only images allowed")

    os.makedirs(settings.MEDIA_PATH, exist_ok=True)

    extension = file.filename.split('.')[-1] if file.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.MEDIA_PATH, filename)

    contents = await file.read()
    with open(filepath, "wb") as f:
        f.write(contents)

    media_id = create_media(db, filepath)

    return {"result": True, "media_id": media_id}