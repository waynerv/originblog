from tortoise import Tortoise, run_async

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


async def run(email: str, password: str):
    await Tortoise.init(db_url=settings.DATABASE_URI, modules={"models": ["app.models.user"]})
    await Tortoise.generate_schemas()

    await User.create(
        email=email,
        name="Admin",
        password_hash=get_password_hash(password),
    )


if __name__ == "__main__":
    print("Creating superuser admin@originblog.com")
    email = input('Please input admin account email(default:admin@originblog.com):') or "admin@originblog.com"
    password = input('Please input admin account password(default:password):') or "password"
    run_async(run(email, password))
    print("Superuser created")
