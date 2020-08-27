from app.core import security
from app.crud.user import get_user_by_email


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not security.verify_password(password, user.password_hash):
        return False
    return user
