from fastapi import APIRouter

from app.api.endpoints import auth, user, post, category, tag

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(user.router, tags=["User"])
api_router.include_router(post.router, tags=["Post"])
api_router.include_router(category.router, tags=["Category"])
api_router.include_router(tag.router, tags=["Tag"])