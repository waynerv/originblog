import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.models.user import User
from app.schemas.user import TokenData
from app.crud.user import get_user_by_email
from app.core import security


async def get_current_user(
        token: str = Depends(security.oauth2_scheme)
) -> User:
    """通过登陆令牌获取当前用户对象"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = await get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user
