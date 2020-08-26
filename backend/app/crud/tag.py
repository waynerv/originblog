from typing import Optional, List

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


async def get(tag_id: int) -> Optional[Tag]:
    """通过id获取指定标签"""
    return await Tag.get(id=tag_id)


async def get_by_name(name: str) -> Optional[Tag]:
    """通过名称能获取指定标签"""
    return await Tag.filter(name=name).first()


async def get_all() -> List[Tag]:
    """获取所有的标签"""
    return await Tag.all().order_by('-id')


async def create(tag_in: TagCreate) -> Tag:
    """创建新的标签"""
    tag = await Tag.create(**tag_in.dict())
    return tag


async def update(tag: Tag, tag_in: TagUpdate) -> Tag:
    """创建新的标签"""
    updated_tag = tag.update_from_dict(tag_in.dict())
    await tag.save()

    return updated_tag


async def delete(tag: Tag) -> None:
    """删除指定的标签"""
    await tag.delete()
