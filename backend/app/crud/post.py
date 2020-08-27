from typing import Optional, List

from fastapi import HTTPException

from app.models.category import Category
from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate
from app.utils.pagination import CollectionResponse, paginate


async def get(post_id: int) -> Optional[Post]:
    """通过id获取指定文章"""
    return await Post.get(id=post_id)


async def get_by_title(title: str) -> Optional[Post]:
    """通过title获取指定文章"""
    return await Post.filter(title=title).first()


async def get_by_slug(slug: str) -> Optional[Post]:
    """通过slug获取指定文章"""
    return await Post.filter(slug=slug).first()


async def get_all() -> List[Post]:
    """获取所有的文章"""
    return await Post.all().order_by('-id')


async def get_multi(page: int, per_page: int, conditions: dict) -> CollectionResponse:
    query = Post
    if conditions.get('title'):
        query = query.filter(title__contains=conditions['title'])
    if conditions.get('type'):
        query = query.filter(type=conditions['type'])
    if conditions.get('is_draft'):
        query = query.filter(is_draft=conditions['is_draft'])
    if conditions.get('category_id'):
        query = query.filter(category_id=conditions['category_id'])
    if conditions.get('tag_id'):
        query = query.filter(tags__id=conditions['tag_id'])

    return await paginate(query, page, per_page)


async def create(post_in: PostCreate, current_user: User) -> Post:
    """创建新的文章"""
    category = await Category.get(id=post_in.category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail='指定的分类不存在'
        )

    post = await Post.create(**post_in.dict(), author=current_user, category=category)

    tags = []
    for tag_id in post_in.tag_ids:
        tag = await Tag.get(id=tag_id)
        if not tag:
            raise HTTPException(
                status_code=404,
                detail='指定的标签不存在'
            )
        tags.append(tag)
    await post.tags.add(*tags)

    return post


async def update(post: Post, post_in: PostUpdate) -> Post:
    """创建新的文章"""
    updated_post = post.update_from_dict(post_in.dict())
    await post.save()

    return updated_post


async def delete(post: Post) -> None:
    """删除指定的文章"""
    await post.delete()
