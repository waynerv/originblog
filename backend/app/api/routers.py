from fastapi import APIRouter

from app.api.endpoints import auth, user, post

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Login"])
api_router.include_router(user.router, prefix="/users", tags=["User"])
api_router.include_router(post.router, tags=["Post"])