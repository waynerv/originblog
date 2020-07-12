from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app import settings
from app.database.session import Session


def register_middleware(app):

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # @app.middleware("http")
    # async def db_session_middleware(request: Request, call_next):
    #     """为每个请求设置数据库会话的中间件"""
    #     request.state.db = Session()
    #     response = await call_next(request)
    #     request.state.db.close()
    #     return response
