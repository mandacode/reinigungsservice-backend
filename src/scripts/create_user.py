import getpass
import asyncio
import datetime

from passlib.context import CryptContext


from db.config import async_session, engine
from domain.models import User
from db.tables import create_tables, run_mappers
from db.repositories import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    username = input("Enter admin username: ").strip()
    password = getpass.getpass("Enter password: ").strip()
    confirm = getpass.getpass("Confirm password: ").strip()

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    hashed_password = pwd_context.hash(password)

    await create_tables(engine=engine)
    run_mappers()

    async with async_session() as db:
        repo = UserRepository(db)
        user = await repo.get_by_username(username)
        if user:
            print("❌ User already exists.")
            return
        user = User(
            username=username,
            password=hashed_password,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        await repo.add(user)
        print("✅ Admin user created successfully.")



if __name__ == "__main__":
    asyncio.run(create_admin_user())
