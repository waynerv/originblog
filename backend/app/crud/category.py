from typing import Optional, List

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get(category_id: int) -> Optional[Category]:
    """通过id获取指定分类"""
    return await Category.get(id=category_id)


async def get_all() -> List[Category]:
    """获取所有的分类"""
    return await Category.all()


async def create(category_in: CategoryCreate) -> Category:
    """创建新的分类"""
    category = await Category.create(**category_in.dict())
    return category


async def update(category: Category, category_in: CategoryUpdate) -> Category:
    """创建新的分类"""
    updated_category = category.update_from_dict(category_in.dict())
    await category.save()

    return updated_category


async def delete(category: Category) -> None:
    """删除指定的分类"""
    await category.delete()
