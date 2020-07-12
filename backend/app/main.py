from fastapi import FastAPI, Depends
import uvicorn

from app.core.config import settings
from app.core.auth import get_current_active_user

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api/openapi.json"
)

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# # Routers
# app.include_router(api_router, prefix='/api',dependencies=[Depends(get_current_active_user)])
#
# # 注册异常处理器、中间件
# register_error_handlers(app)
#
# @app.get("/api/v1")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/api/v1/task")
# async def example_task():
#     celery_app.send_task("app.tasks.example_task", args=["Hello World"])
#
#     return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
