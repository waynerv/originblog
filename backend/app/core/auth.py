from app.core import security
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not security.verify_password(password, user.password_hash):
        return False
    return user


def sign_up_new_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if user:
        return False  # User already exists
    new_user = create_user(
        db,
        UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
        ),
    )
    return new_user
