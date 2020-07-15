from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., title='分类名称', max_length=32)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
