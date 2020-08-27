from datetime import datetime
from enum import IntEnum
from typing import List

from pydantic import Field
from pydantic.main import BaseModel

from app.schemas.common import CollectionOut


class PostType(IntEnum):
    article = 1
    about = 2


class PostBase(BaseModel):
    title: str = Field(..., title='标题', max_length=255)
    summary: str = Field(..., title='摘要', max_length=255)
    slug: str = Field(..., title='Slug', max_length=128)
    content: str = Field(..., title='正文')
    type: PostType = Field(1, title='类型')
    is_draft: bool = Field(False, title='是否为草稿')
    can_comment: bool = Field(True, title='是否允许评论')
    category_id: int = Field(..., title='分类id')


class PostCreate(PostBase):
    tag_ids: List[int] = Field(..., title='标签id集合')

    class Config:
        use_enum_values = True


class PostUpdate(PostCreate):
    pass


class PostBaseOut(PostBase):
    id: int
    created_at: datetime = Field(..., title='创建时间')
    updated_at: datetime = Field(..., title='最后更新时间')

    class Config:
        orm_mode = True


class PostOut(PostBaseOut):
    pass


class PostPageOut(PostBaseOut):
    pass


class PostPage(CollectionOut):
    data: List[PostPageOut]
