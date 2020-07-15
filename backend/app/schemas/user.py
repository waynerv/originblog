from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., title='邮箱', max_length=64)
    name: str = Field(..., title='姓名', max_length=64)
    avatar: str = Field(..., title='头像地址', max_length=128)


class UserUpdate(UserBase):
    password: str = Field(None, title='密码', max_length=16)


class UserCreate(UserUpdate):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
