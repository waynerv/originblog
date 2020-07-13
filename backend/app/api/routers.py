from fastapi import APIRouter

from app.api.endpoints import auth, user

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])