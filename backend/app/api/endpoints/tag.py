from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.db_helper import get_db
from app.schemas.auth import UserProfile
from app.schemas.tag import TagOut, TagCreate, TagUpdate
from app.utils.response import ERROR_404, ERROR_403, ERROR_400


router = APIRouter()


# -----------------------Tag Collection API-----------------------

@router.get('/tags', response_model=List[TagOut], responses={**ERROR_404})
async def read_tags(
        *,
        db: Session = Depends(get_db),
):
    """获取标签列表"""
    tags = await crud.tag.get_multi(db)

    return tags


@router.post('/tags', status_code=201, response_model=TagOut, responses={**ERROR_404})
async def create_tag(
        *,
        db: Session = Depends(get_db),
        tag_in: TagCreate,
        current_user: UserProfile = Depends(get_current_user),
):
    """创建新标签"""
    tag = crud.tag.create(db, tag_in=tag_in, creator_id=current_user.id)

    return tag


# -----------------------Tag API------------------------

@router.put('/tags/{tag_id}', status_code=200, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def update_tag(
        *,
        db: Session = Depends(get_db),
        tag_in: TagUpdate,
        current_user: UserProfile = Depends(get_current_user),
):
    """修改标签"""
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail='修改的工单不存在'
        )


    crud.tag.update(db, tag=tag, tag_in=tag_in)



@router.delete('/tags/{tag_id}', status_code=204, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def delete_tag(
        *,
        db: Session = Depends(get_db),
        tag_id: int,
        current_user: UserProfile = Depends(get_current_user)
):
    """删除标签"""
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail='该工单不存在'
        )

    crud.tag.delete(db, tag=tag)