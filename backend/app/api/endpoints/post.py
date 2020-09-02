from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.db_helper import get_db
from app.api.dependencies.query_helper import get_post_conditions
from app.models.user import User
from app.schemas.post import PostPage, PostBaseOut, PostOut, PostUpdate, PostCreate
from app.utils.response import ERROR_404

router = APIRouter()


# -----------------------Post Collection API-----------------------

@router.get('/posts', response_model=PostPage, responses={**ERROR_404})
async def read_posts(
        page: int,
        per_page: int,
        conditions: dict = Depends(get_post_conditions),
):
    """获取文章列表"""
    posts = await crud.post.get_multi(page=page, per_page=per_page, conditions=conditions)

    return posts


@router.post('/posts', status_code=201, response_model=PostBaseOut, responses={**ERROR_404})
async def create_post(
        post_in: PostCreate,
        current_user: User = Depends(get_current_user)
):
    """新增文章"""
    same_title_post = await crud.post.get_by_title(post_in.title)
    if same_title_post:
        raise HTTPException(
            status_code=400,
            detail='已存在相同标题文章'
        )

    same_slug_post = await crud.post.get_by_slug(post_in.slug)
    if same_slug_post:
        raise HTTPException(
            status_code=400,
            detail='已存在相同Slug文章'
        )

    post = await crud.post.create(post_in, current_user)

    return post


# -----------------------Post API------------------------

@router.get('/posts/{post_id}', response_model=PostOut, responses={**ERROR_404})
def read_post_by_id(
        *,
        db: Session = Depends(get_db),
        post_id: int,
):
    """获取文章详情"""
    post = crud.post.get(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail='该变更不存在'
        )

    return post


@router.put('/posts/{post_id}', status_code=200, responses={**ERROR_404})
def update_post(
        *,
        db: Session = Depends(get_db),
        post_id: int,
        post_in: PostUpdate,
        current_user: User = Depends(get_current_user)
):
    """更新文章详情"""
    post = crud.post.get(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail='修改的变更不存在'
        )

    crud.post.update(db, db_obj=post, obj_in=post_in)


@router.delete('/posts/{post_id}', status_code=204, responses={**ERROR_404})
def delete_post(
        *,
        db: Session = Depends(get_db),
        post_id: int,
        current_user: User = Depends(get_current_user)
):
    """删除文章"""
    post = crud.post.get(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail='指定的变更不存在'
        )

    crud.post.delete(db, db_obj=post)
