from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.tag import TagOut, TagCreate, TagUpdate
from app.utils.response import ERROR_404, ERROR_403, ERROR_400

router = APIRouter()


# -----------------------Tag Collection API-----------------------

@router.get('/tags', response_model=List[TagOut], responses={**ERROR_404})
async def read_tags():
    """获取标签列表"""
    tags = await crud.tag.get_all()

    return tags


@router.post('/tags', status_code=201, response_model=TagOut, responses={**ERROR_404})
async def create_tag(
        tag_in: TagCreate,
        current_user: User = Depends(get_current_user),
):
    """创建新标签"""
    tag = await crud.tag.create(tag_in=tag_in)

    return tag


# -----------------------Tag API------------------------

@router.get('/tags/{tag_id}', response_model=TagOut, responses={**ERROR_404})
async def read_tag_by_id(
        tag_id: int
):
    """获取标签列表"""
    tag = await crud.tag.get(tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail='指定的标签不存在'
        )

    return tag


@router.put('/tags/{tag_id}', status_code=200, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def update_tag(
        tag_id: int,
        tag_in: TagUpdate,
        current_user: User = Depends(get_current_user),
):
    """修改标签"""
    tag = await crud.tag.get(tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail='指定的标签不存在'
        )

    await crud.tag.update(tag, tag_in=tag_in)


@router.delete('/tags/{tag_id}', status_code=204, responses={**ERROR_400, **ERROR_403, **ERROR_404})
async def delete_tag(
        tag_id: int,
        current_user: User = Depends(get_current_user)
):
    """删除标签"""
    tag = await crud.tag.get(tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail='指定的标签不存在'
        )

    await crud.tag.delete(tag)
