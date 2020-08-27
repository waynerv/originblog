"""Simple helper to paginate query
"""
from math import ceil
from typing import Dict, Optional, Union, List, Any

from tortoise import QuerySet

from app.utils.exception import NotFoundError, ValidationError

DEFAULT_PAGE_SIZE = 30
DEFAULT_PAGE_NUMBER = 1

CollectionResponse = Dict[str, Union[List[Optional[Any]], Optional[dict]]]


async def paginate(query: QuerySet, page: int, per_page: int) -> CollectionResponse:
    """Returns ``per_page`` items from page ``page``.

    the following rules will raise a 404 error:
    * No items are found and ``page`` is not 1.
    * ``page`` is less than 1, or ``per_page`` is negative.
    * ``page`` or ``per_page`` are not ints.

    Returns a :type:`CollectionResponse` dict.
    """
    if page < 1:
        raise NotFoundError('查询页面的资源不存在')

    if per_page < 0:
        raise NotFoundError('查询页面的资源不存在')

    if per_page > 100:
        raise ValidationError('超出最大每页可获取资源数量')

    items = await query.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1:
        raise NotFoundError

    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = await query.count()

    if per_page == 0 or total == 0:
        pages = 0
    else:
        pages = int(ceil(total / float(per_page)))

    return {
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'pages': pages,
            'total': total
        }
    }
