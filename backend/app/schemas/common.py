from typing import Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int
    per_page: int
    pages: int
    total: int


class ErrorOut(BaseModel):
    type: str
    message: str
    status: int
    detail: Optional[list] = None


class CollectionOut(BaseModel):
    data: list
    pagination: Pagination = None


class EmployeeBase(BaseModel):
    id: int = Field(..., title="ID")
    name: str = Field(..., title="名称")
    serial: str = Field(None, title="工号")

    class Config:
        orm_mode = True


class EmployeeOut(EmployeeBase):
    phone: str = Field(None, title="手机号码")
    mail: str = Field(None, title="邮箱")
    avatar: str = Field(None, title="头像url")
