from fastapi import APIRouter

from app.api.endpoints import auth, users

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])