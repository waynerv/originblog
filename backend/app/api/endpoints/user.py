from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.crud.user import edit_user
from app.schemas.user import UserUpdate, UserOut

router = APIRouter()


@router.get("/users/me", response_model=UserOut, response_model_exclude_none=True)
async def get_current_user(current_user=Depends(get_current_user)):
    """获取当前用户详情"""
    return current_user


@router.put(
    "/users/me", response_model=UserOut, response_model_exclude_none=True
)
async def update_current_user(
        user_in: UserUpdate,
        current_user=Depends(get_current_user),
):
    """修改当前用户信息"""
    return await edit_user(current_user, user_in)
