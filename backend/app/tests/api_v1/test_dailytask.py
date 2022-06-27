from httpx import AsyncClient
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.main import app
from app.tests.utils.users import cr_rand_user, user_token
from app.tests.utils.utils import BURL, compare


@pytest.mark.anyio
async def test_dailytask_get(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dailytask = schemas.SDailyTaskCreate(name="test")
    await crud.dailytask.create(db, uid, obj_in=dailytask)

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/dailytask/")
    assert r.status_code == 200
    web_res = r.json()
    assert len(web_res) == 1
    compare(schemas.SDailyTaskCreate, web_res[0], dailytask)
    # TODO: Add check of states creation/deletion


@pytest.mark.anyio
async def test_dailytask_update(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    create = schemas.SDailyTaskCreate(name="test")
    update = {"name": "test2", "is_active": False}
    dt_uid = (await crud.dailytask.create(db, uid, obj_in=create)).uid

    # Correct update
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/dailytask/{dt_uid}", json=update)
    assert r.status_code == 200
    assert r.json()["state"]
    db.expire_all()
    dailytask = await crud.dailytask.get(db, uid, uid=dt_uid)
    assert dailytask is not None
    compare(schemas.SDailyTaskUpdate, dailytask, update)

    # Update non-existent record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/dailytask/{dt_uid+1}", json=update)
    assert r.status_code == 404

    # Update other user record
    uid2 = (await cr_rand_user(db)).uid
    dt_uid2 = (await crud.dailytask.create(db, uid2, obj_in=create)).uid
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/dailytask/{dt_uid2}", json=update)
    assert r.status_code == 403
    db.expire_all()
    dailytask = await crud.dailytask.get(db, uid2, uid=dt_uid2)
    assert dailytask is not None
    compare(schemas.SDailyTaskUpdate, dailytask, create)


@pytest.mark.anyio
async def test_dailytask_create(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dailytask = {"name": "test", "is_active": True}

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.post("/dailytask/", json=dailytask)
    assert r.status_code == 200
    web_res = r.json()
    compare(schemas.SDailyTaskCreate, web_res, dailytask)
    db.expire_all()
    db_res = await crud.dailytask.get(db, uid, uid=web_res["uid"])
    assert db_res is not None
    compare(schemas.SDailyTaskCreate, db_res, web_res)


@pytest.mark.anyio
async def test_dailytask_delete(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    create = schemas.SDailyTaskCreate(name="test")
    dt_uid = (await crud.dailytask.create(db, uid, obj_in=create)).uid

    # Correct deletion
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/dailytask/{dt_uid}")
    assert r.status_code == 200
    assert r.json()["state"]
    db.expire_all()
    db_res = await crud.dailytask.get(db, uid, uid=dt_uid)
    assert db_res is None

    # Delete non-existent record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/dailytask/{dt_uid}")
    assert r.status_code == 404

    # Delete other user record
    uid2 = (await cr_rand_user(db)).uid
    dt_uid2 = (await crud.dailytask.create(db, uid2, obj_in=create)).uid
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/dailytask/{dt_uid2}")
    assert r.status_code == 403
    db.expire_all()
    dailytask = await crud.dailytask.get(db, uid2, uid=dt_uid2)
    assert dailytask is not None
    compare(schemas.SDailyTaskUpdate, dailytask, create)
