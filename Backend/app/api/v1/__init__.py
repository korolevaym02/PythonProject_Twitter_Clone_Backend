from fastapi import APIRouter
from .endpoints import tweets, users, medias

api_router = APIRouter()
api_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(medias.router, prefix="/medias", tags=["medias"])