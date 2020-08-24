from tortoise import Tortoise, run_async

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


async def run():
    await Tortoise.init(db_url=settings.DATABASE_URI, modules={"models": ["app.models.user"]})
    await Tortoise.generate_schemas()

    await User.create(
        email="admin@originblog.com",
        name="Admin",
        password_hash=get_password_hash("password"),
    )


if __name__ == "__main__":
    print("Creating superuser admin@originblog.com")
    run_async(run())
    print("Superuser created")
