from httpx import AsyncClient
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.security import verify_password
from app.main import app
from app.tests.utils.users import create_random_user, user_token
from app.tests.utils.utils import BURL, compare


@pytest.mark.anyio
async def test_user_get_multi(db: AsyncSession, superuser: models.User) -> None:
    # Superuser receive all users
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 200
    all_users = r.json()
    assert len(all_users) == 1
    compare(schemas.SUser, all_users[0], superuser)

    await create_random_user(db, email="a@nottest.test")
    await create_random_user(db, is_superuser=True)
    await create_random_user(db)

    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 200
    all_users = r.json()
    assert len(all_users) == 4


@pytest.mark.anyio
async def test_user_get_multi_forbiden(db: AsyncSession, reguser: models.User) -> None:
    # Not superuser
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 400

    # Inactive
    user = await create_random_user(db, is_active=False, is_superuser=True)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(user)) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 400

    # Fake
    async with AsyncClient(app=app, base_url=BURL, headers={"Authorization": "Bearer fake_token"}) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 403

    # Unauthorized
    async with AsyncClient(app=app, base_url=BURL) as ac:
        r = await ac.get("/users/")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_user_create(db: AsyncSession, superuser: models.User) -> None:
    # Superuser create user
    user = schemas.SUserCreate(full_name="test", password="test", email="test@test.test")
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.post("/users/", json=user.dict())
    assert r.status_code == 200
    newuser = r.json()
    await db.commit()
    dbuser = await crud.user.get(db, uid=newuser["uid"])
    assert dbuser is not None
    dbuser.password = ""    # type: ignore
    compare(schemas.SUserCreate, r.json() | {"password": ""}, user, exclude=["password"])
    compare(schemas.SUserCreate, dbuser, user, exclude=["password"])
    assert verify_password("test", dbuser.hashed_password)
    assert dbuser.is_superuser is False


@pytest.mark.anyio
async def test_user_create_forbiden(db: AsyncSession, reguser: models.User) -> None:
    # Regular user can't create user
    user = schemas.SUserCreate(full_name="test", password="test", email="test@test.test")
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.post("/users/", json=user.dict())
    assert r.status_code == 400

    # Unauthorized user can't create user
    user = schemas.SUserCreate(full_name="test", password="test", email="test@test.test")
    async with AsyncClient(app=app, base_url=BURL) as ac:
        r = await ac.post("/users/", json=user.dict())
    assert r.status_code == 401


@pytest.mark.anyio
async def test_user_create_duplicate(db: AsyncSession, superuser: models.User) -> None:
    # Refuse email duplicates
    await create_random_user(db, email="test@test.test")
    user = schemas.SUserCreate(full_name="test", password="test", email="test@test.test")
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.post("/users/", json=user.dict())
    assert r.status_code == 409


# TODO: Add coretask, coreactivity update check
@pytest.mark.anyio
async def test_user_update_self(db: AsyncSession, reguser: models.User) -> None:
    update = {"full_name": "full_name", "password": "password"}
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.put("/users/me", json=update)
    assert r.status_code == 200
    await db.refresh(reguser)
    assert reguser.full_name == "full_name"
    assert verify_password("password", reguser.hashed_password)
    compare(schemas.SUser, reguser, r.json())


@pytest.mark.anyio
async def test_user_get_self(db: AsyncSession, reguser: models.User) -> None:
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.get("/users/me")
    assert r.status_code == 200
    compare(schemas.SUser, reguser, r.json())


@pytest.mark.anyio
async def test_user_get_by_id(db: AsyncSession, reguser: models.User) -> None:
    # Self account
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.get(f"/users/{reguser.uid}")
    assert r.status_code == 200
    compare(schemas.SUser, reguser, r.json())

    # Other user account
    user = await create_random_user(db)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.get(f"/users/{user.uid}")
    assert r.status_code == 403

    # Missing account
    uid = user.uid
    await crud.user.remove(db, uid=uid)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.get(f"/users/{uid}")
    assert r.status_code == 403


@pytest.mark.anyio
async def test_user_get_by_id_super(db: AsyncSession, superuser: models.User) -> None:
    # Self account
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.get(f"/users/{superuser.uid}")
    assert r.status_code == 200
    compare(schemas.SUser, superuser, r.json())

    # Other user account
    user = await create_random_user(db)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.get(f"/users/{user.uid}")
    assert r.status_code == 200
    compare(schemas.SUser, user, r.json())

    # Missing account
    uid = user.uid
    await crud.user.remove(db, uid=uid)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.get(f"/users/{uid}")
    assert r.status_code == 404


# TODO: Add coretask, coreactivity update check
@pytest.mark.anyio
async def test_user_update_super(db: AsyncSession, superuser: models.User) -> None:
    user = await create_random_user(db)
    update = schemas.SUserAdminUpdate(
        full_name="full_name",
        password="password",
        email="newmail@test.test",
        is_active=False,
        is_superuser=True,
    )
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.put(f"/users/{user.uid}", json=update.dict())
    assert r.status_code == 200
    await db.refresh(user)
    assert user.full_name == "full_name"
    assert user.email == "newmail@test.test"
    assert user.is_active is False
    assert user.is_superuser is True
    assert verify_password("password", user.hashed_password)
    compare(schemas.SUser, user, r.json())


@pytest.mark.anyio
async def test_user_update_duplicate(db: AsyncSession, superuser: models.User) -> None:
    user = await create_random_user(db)
    update = schemas.SUserAdminUpdate(email=superuser.email)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.put(f"/users/{user.uid}", json=update.dict())
    assert r.status_code == 409


@pytest.mark.anyio
async def test_user_update_forbiden(db: AsyncSession, reguser: models.User) -> None:
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.put(f"/users/{reguser.uid}", json={"full_name": "name"})
    assert r.status_code == 400


@pytest.mark.anyio
async def test_user_delete(db: AsyncSession, superuser: models.User) -> None:
    uid = (await create_random_user(db)).uid
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.delete(f"/users/{uid}")
    assert r.status_code == 200
    user2 = await crud.user.get(db, uid=uid)
    assert user2 is None

    # Missed UID
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(superuser)) as ac:
        r = await ac.delete(f"/users/{uid}")
    assert r.status_code == 404


@pytest.mark.anyio
async def test_user_delete_forbiden(db: AsyncSession, reguser: models.User) -> None:
    user = await create_random_user(db)
    async with AsyncClient(app=app, base_url=BURL, headers=user_token(reguser)) as ac:
        r = await ac.delete(f"/users/{user.uid}")
    assert r.status_code == 400
