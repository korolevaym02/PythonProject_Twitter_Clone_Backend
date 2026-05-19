from pydantic import BaseModel


class MediaResponse(BaseModel):
    result: bool
    media_id: int