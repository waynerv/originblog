from typing import Optional

from fastapi import HTTPException

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserUpdate


async def get_user(user_id: int):
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(email: str) -> Optional[User]:
    user = await User.filter(email=email).first()
    return user


async def edit_user(
        user: User, user_in: UserUpdate
) -> User:
    update_data = user_in.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(user_in.password)
        del update_data["password"]

    updated_user =  user.update_from_dict(update_data)
    await user.save()

    return updated_user
