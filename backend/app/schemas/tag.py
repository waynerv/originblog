from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., title='标签名称', max_length=32)


class TagCreate(TagBase):
    pass


class TagUpdate(TagCreate):
    pass


class TagOut(TagBase):
    id: int

    class Config:
        orm_mode = True