from datetime import datetime, timedelta
from fastapi import HTTPException
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.core.security import verify_password
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_string


@pytest.mark.anyio
async def test_user_get_by_email(db: AsyncSession, cleandb) -> None:
    user1 = await create_random_user(db)
    user2 = await crud.user.get_by_email(db, email=user1.email)
    assert user1 == user2


@pytest.mark.anyio
async def test_user_get_by_email_missing(db: AsyncSession, cleandb) -> None:
    user = await crud.user.get_by_email(db, email="none")
    assert user is None


@pytest.mark.anyio
async def test_user_get_demo(db: AsyncSession, cleandb) -> None:
    # Demo-mode disabled, result allways empty
    settings.DEMO_USERS = 0
    created_dt = datetime.now() - timedelta(minutes=settings.DEMO_ACCESS_TOKEN_EXPIRE_MINUTES + 5)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 0

    await create_random_user(db, created_dt=created_dt)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 0

    # Demo-mode disabled, result is expired demo account list
    settings.DEMO_USERS = 100
    users = await crud.user.get_demo_users(db)
    assert len(users) == 1

    await create_random_user(db, created_dt=created_dt)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 2

    await create_random_user(db)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 2

    await create_random_user(db, email="a@nottest.test", created_dt=created_dt)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 2

    await create_random_user(db, is_superuser=True, created_dt=created_dt)
    users = await crud.user.get_demo_users(db)
    assert len(users) == 2


@pytest.mark.anyio
async def test_user_get_count(db: AsyncSession, cleandb) -> None:
    cnt = await crud.user.get_count(db)
    assert cnt == 0
    await create_random_user(db, email="a@nottest.test")
    await create_random_user(db, is_superuser=True)
    await create_random_user(db)
    cnt = await crud.user.get_count(db)
    assert cnt == 3


@pytest.mark.anyio
async def test_user_create(db: AsyncSession, cleandb) -> None:
    email = random_string() + "@test.test"
    password = random_string()
    full_name = random_string()
    user_in = schemas.SUserCreate(email=email, password=password, full_name=full_name)
    user = await crud.user.create(db, obj_in=user_in, data_source=None)
    assert user.email == email
    assert user.full_name == full_name
    assert hasattr(user, "hashed_password")


@pytest.mark.anyio
async def test_user_create_dataset(db: AsyncSession, cleandb) -> None:
    email = random_string() + "@test.test"
    password = random_string()
    full_name = random_string()
    user_in = schemas.SUserCreate(email=email, password=password, full_name=full_name)
    user = await crud.user.create(db, obj_in=user_in, data_source="init.json")
    assert user.email == email
    email = random_string() + "@test.test"
    user_in = schemas.SUserCreate(email=email, password=password, full_name=full_name)
    user = await crud.user.create(db, obj_in=user_in, data_source="demo.json")
    assert user.email == email


@pytest.mark.anyio
async def test_user_create_double(db: AsyncSession, cleandb) -> None:
    # Duplicate Email raise exception
    user = await create_random_user(db)
    user_in = schemas.SUserCreate(email=user.email, password=user.hashed_password, full_name=user.full_name)
    with pytest.raises(HTTPException) as err:
        await crud.user.create(db, obj_in=user_in, data_source=None)
    assert err.value.status_code == 409


@pytest.mark.anyio
async def test_user_get(db: AsyncSession, cleandb) -> None:
    # Test correct uid
    user = await create_random_user(db)
    user2 = await crud.user.get(db, uid=user.uid, r404=True)
    assert user == user2

    # Test missing uid
    user2 = await crud.user.get(db, uid=0)
    assert user2 is None

    with pytest.raises(HTTPException) as err:
        await crud.user.get(db, uid=0, r404=True)
    assert err.value.status_code == 404


@pytest.mark.anyio
async def test_user_get_multi(db: AsyncSession, cleandb) -> None:
    users = await crud.user.get_multi(db)
    assert len(users) == 0
    await create_random_user(db, email="a@nottest.test")
    await create_random_user(db, is_superuser=True)
    await create_random_user(db)
    users = await crud.user.get_multi(db)
    assert len(users) == 3


@pytest.mark.anyio
async def test_user_remove(db: AsyncSession, cleandb) -> None:
    cnt = await crud.user.get_count(db)
    assert cnt == 0

    await create_random_user(db)
    user = await create_random_user(db)
    await create_random_user(db)
    cnt = await crud.user.get_count(db)
    assert cnt == 3
    uid = user.uid

    removed = await crud.user.remove(db, uid=uid)
    assert removed == 1
    cnt = await crud.user.get_count(db)
    assert cnt == 2
    user2 = await crud.user.get(db, uid=uid)
    assert user2 is None


@pytest.mark.anyio
async def test_user_remove_missing(db: AsyncSession, cleandb) -> None:
    # Try remove missing uid
    uid = 10
    removed = await crud.user.remove(db, uid=uid)
    assert removed == 0

    with pytest.raises(HTTPException) as err:
        await crud.user.remove(db, uid=uid, r404=True)
    assert err.value.status_code == 404


@pytest.mark.anyio
async def test_user_update(db: AsyncSession, cleandb) -> None:
    user = await create_random_user(db)
    uid = user.uid

    # Update by dict
    user1 = await crud.user.update(
        db,
        uid=uid,
        obj_in={"full_name": "name", "password": "password"},
    )
    user2 = await crud.user.get(db, uid=uid)
    assert user1 == user2
    assert user2 is not None
    assert user2.full_name == "name"
    assert verify_password("password", user2.hashed_password)

    # Update by schema
    user1 = await crud.user.update(
        db,
        uid=uid,
        obj_in=schemas.SUserUpdate(full_name="name2", password="password2"),
    )
    user3 = await crud.user.get(db, uid=uid)
    assert user1 == user3
    assert user3 is not None
    assert user3.full_name == "name2"
    assert verify_password("password2", user3.hashed_password)


@pytest.mark.anyio
async def test_user_update_missing(db: AsyncSession, cleandb) -> None:
    # Try update missing uid
    uid = 10
    with pytest.raises(HTTPException) as err:
        await crud.user.update(
            db,
            uid=uid,
            obj_in={"full_name": "name", "password": "password"},
        )
    assert err.value.status_code == 404

    with pytest.raises(HTTPException) as err:
        await crud.user.update(
            db,
            uid=uid,
            obj_in=schemas.SUserUpdate(full_name="name2", password="password2"),
        )
    assert err.value.status_code == 404


@pytest.mark.anyio
async def test_user_update_duplicate(db: AsyncSession, cleandb) -> None:
    await create_random_user(db, email="test@test.test")
    uid = (await create_random_user(db)).uid
    with pytest.raises(HTTPException) as err:
        await crud.user.update(
            db,
            uid=uid,
            obj_in={"email": "test@test.test"},
        )
    assert err.value.status_code == 409


@pytest.mark.anyio
async def test_user_update_byobj(db: AsyncSession, cleandb) -> None:
    user = await create_random_user(db)
    uid = user.uid

    # Update by dict
    user1 = await crud.user.update_byobj(
        db,
        db_obj=user,
        obj_in={"full_name": "name", "password": "password"},
    )
    user2 = await crud.user.get(db, uid=uid)
    assert user1 == user2
    assert user2 is not None
    assert user2.full_name == "name"
    assert verify_password("password", user2.hashed_password)

    # Update by schema
    user1 = await crud.user.update_byobj(
        db,
        db_obj=user,
        obj_in=schemas.SUserUpdate(full_name="name2", password="password2"),
    )
    user3 = await crud.user.get(db, uid=uid)
    assert user1 == user3
    assert user3 is not None
    assert user3.full_name == "name2"
    assert verify_password("password2", user3.hashed_password)


@pytest.mark.anyio
async def test_user_update_byobj_duplicate(db: AsyncSession, cleandb) -> None:
    await create_random_user(db, email="test@test.test")
    user = await create_random_user(db)

    # Update by dict
    with pytest.raises(HTTPException) as err:
        await crud.user.update_byobj(
            db,
            db_obj=user,
            obj_in={"email": "test@test.test"},
        )
    assert err.value.status_code == 409


@pytest.mark.anyio
async def test_user_authenticate(db: AsyncSession, cleandb) -> None:
    # Check correct and incorrect credentials
    user = await create_random_user(db, email="test@test.test", password="test")
    user2 = await crud.user.authenticate(db, email="test@test.test", password="test")
    assert user == user2
    user2 = await crud.user.authenticate(db, email="test@test.test", password="test1")
    assert user2 is None
    user2 = await crud.user.authenticate(db, email="aaaa@test.test", password="test")
    assert user2 is None
