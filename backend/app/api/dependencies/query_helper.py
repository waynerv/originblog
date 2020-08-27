from typing import Union, Dict

from fastapi import Query

from app.schemas.post import PostType


def get_post_conditions(
        title: str = Query(None, description='标题'),
        type: PostType = Query(int(PostType.article), description='类型'),
        is_draft: bool = Query(False, description='是否为草稿'),
        category_id: int = Query(None, description='分类id'),
        tag_id: int = Query(None, description='标签id'),
) -> Dict[str, Union[str, int, None]]:
    return {
        'title': title,
        'type': type,
        'is_draft': is_draft,
        'category_id': category_id,
        'tag_id': tag_id,
    }
