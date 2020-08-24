from starlette.responses import UJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from app.api.routers import api_router
from app.errorhandlers import register_error_handlers
from fastapi import FastAPI
import uvicorn

from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(api_router, prefix='/api', default_response_class=UJSONResponse)

# 注册异常处理器、中间件
register_error_handlers(app)

@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": ["app.models.category", "app.models.tag", "app.models.user", "app.models.post"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True, port=8080)
