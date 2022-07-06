from typing import AsyncGenerator
import pytest   # type: ignore
from sqlalchemy import MetaData, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base
from app.db.session import engine
from app.models import User
from app.tests.utils.users import cr_rand_user


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
async def recreate_db() -> AsyncGenerator:
    async with engine.begin() as conn:
        meta = MetaData()
        await conn.run_sync(meta.reflect)
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture(scope="session")
async def db(recreate_db) -> AsyncGenerator:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    i = 0
    async with async_session() as session:
        i += 1
        yield session


@pytest.fixture
async def cleandb(db) -> None:
    # Close transaction, if previous test failed
    try:
        await db.commit()
    except Exception:
        await db.rollback()
    await db.execute(delete(User))
    await db.commit()


@pytest.fixture
async def superuser(db, cleandb) -> User:
    user = await cr_rand_user(db, email="super@test.test", is_superuser=True, password="super")
    return user


@pytest.fixture
async def reguser(db, cleandb) -> User:
    user = await cr_rand_user(db, email="regular@test.test", is_superuser=False, password="regular")
    return user
