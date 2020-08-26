from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.category import CategoryOut, CategoryCreate, CategoryUpdate
from app.utils.response import ERROR_404, ERROR_403, ERROR_400

router = APIRouter()


# -----------------------Category Collection API-----------------------

@router.get('/categories', response_model=List[CategoryOut], responses={**ERROR_404})
async def read_categories():
    """获取分类列表"""
    categories = await crud.category.get_all()

    return categories


@router.post('/categories', status_code=201, response_model=CategoryOut, responses={**ERROR_404})
async def create_category(
        category_in: CategoryCreate,
        current_user: User = Depends(get_current_user),
):
    """创建新分类"""
    category = await crud.category.create(category_in=category_in)

    return category


# -----------------------Category API------------------------

@router.get('/categories/{category_id}', response_model=CategoryOut, responses={**ERROR_404})
async def read_category_by_id(
        category_id: int
):
    """获取分类列表"""
    category = await crud.category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='指定的分类不存在'
        )

    return category


@router.put('/categories/{category_id}', status_code=200, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def update_category(
        category_id: int,
        category_in: CategoryUpdate,
        current_user: User = Depends(get_current_user),
):
    """修改分类"""
    category = await crud.category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='指定的分类不存在'
        )

    await crud.category.update(category, category_in=category_in)


@router.delete('/categories/{category_id}', status_code=204, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def delete_category(
        category_id: int,
        current_user: User = Depends(get_current_user)
):
    """删除分类"""
    category = await crud.category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='指定的分类不存在'
        )

    await crud.category.delete(category)
