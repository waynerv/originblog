from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.db_helper import get_db
from app.models.user import User
from app.schemas.category import CategoryOut, CategoryCreate, CategoryUpdate
from app.utils.response import ERROR_404, ERROR_403, ERROR_400


router = APIRouter()


# -----------------------Category Collection API-----------------------

@router.get('/categories', response_model=List[CategoryOut], responses={**ERROR_404})
async def read_categories(
        *,
        db: Session = Depends(get_db),
):
    """获取分类列表"""
    categories = await crud.category.get_multi(db)

    return categories


@router.post('/categories', status_code=201, response_model=CategoryOut, responses={**ERROR_404})
async def create_category(
        *,
        db: Session = Depends(get_db),
        category_in: CategoryCreate,
        current_user: User = Depends(get_current_user),
):
    """创建新分类"""
    category = crud.category.create(db, category_in=category_in, creator_id=current_user.id)

    return category


# -----------------------Category API------------------------

@router.put('/categories/{category_id}', status_code=200, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def update_category(
        *,
        db: Session = Depends(get_db),
        category_in: CategoryUpdate,
        current_user: User = Depends(get_current_user),
):
    """修改分类"""
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='修改的工单不存在'
        )


    crud.category.update(db, category=category, category_in=category_in, is_submit=is_submit)



@router.delete('/categories/{category_id}', status_code=204, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def delete_category(
        *,
        db: Session = Depends(get_db),
        category_id: int,
        current_user: User = Depends(get_current_user)
):
    """删除分类"""
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='该工单不存在'
        )

    crud.category.delete(db, category=category)