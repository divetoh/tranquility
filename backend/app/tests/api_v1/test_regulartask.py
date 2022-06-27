from datetime import date
from httpx import AsyncClient
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.main import app
from app.tests.utils.users import cr_rand_user, user_token
from app.tests.utils.utils import BURL, compare


@pytest.mark.anyio
async def test_regulartask_get(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    regulartask = schemas.SRegularTaskCreate(name="test", is_active=True, nextdate=date(2022, 1, 1), period=10)
    await crud.regulartask.create(db, uid, obj_in=regulartask)

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/regulartask/")
    assert r.status_code == 200
    web_res = r.json()
    assert len(web_res) == 1
    compare(schemas.SRegularTaskCreate, web_res[0], regulartask)


@pytest.mark.anyio
async def test_regulartask_update(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    create = schemas.SRegularTaskCreate(name="test", is_active=True, nextdate=date(2022, 1, 1), period=10)
    update = {"name": "test2", "is_active": False, "nextdate": "2022-01-02", "period": 12}
    rt_uid = (await crud.regulartask.create(db, uid, obj_in=create)).uid

    # Correct update
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/regulartask/{rt_uid}", json=update)
    assert r.status_code == 200
    assert r.json()["state"]
    db.expire_all()
    regulartask = await crud.regulartask.get(db, uid, uid=rt_uid)
    assert regulartask is not None
    compare(schemas.SRegularTaskUpdate, regulartask, update)

    # Update non-existent record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/regulartask/{rt_uid+1}", json=update)
    assert r.status_code == 404

    # Update other user record
    uid2 = (await cr_rand_user(db)).uid
    rt_uid2 = (await crud.regulartask.create(db, uid2, obj_in=create)).uid
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put(f"/regulartask/{rt_uid2}", json=update)
    assert r.status_code == 403
    db.expire_all()
    regulartask = await crud.regulartask.get(db, uid2, uid=rt_uid2)
    assert regulartask is not None
    compare(schemas.SRegularTaskUpdate, regulartask, create)


@pytest.mark.anyio
async def test_regulartask_create(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    regulartask = {"name": "test2", "is_active": False, "nextdate": "2022-01-02", "period": 12}

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.post("/regulartask/", json=regulartask)
    assert r.status_code == 200
    web_res = r.json()
    compare(schemas.SRegularTaskCreate, web_res, regulartask)
    db.expire_all()
    db_res = await crud.regulartask.get(db, uid, uid=web_res["uid"])
    assert db_res is not None
    compare(schemas.SRegularTaskCreate, db_res, web_res)


@pytest.mark.anyio
async def test_regulartask_delete(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    create = schemas.SRegularTaskCreate(name="test", is_active=True, nextdate=date(2022, 1, 1), period=10)
    rt_uid = (await crud.regulartask.create(db, uid, obj_in=create)).uid

    # Correct deletion
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/regulartask/{rt_uid}")
    assert r.status_code == 200
    assert r.json()["state"]
    db.expire_all()
    db_res = await crud.regulartask.get(db, uid, uid=rt_uid)
    assert db_res is None

    # Delete non-existent record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/regulartask/{rt_uid}")
    assert r.status_code == 404

    # Delete other user record
    uid2 = (await cr_rand_user(db)).uid
    rt_uid2 = (await crud.regulartask.create(db, uid2, obj_in=create)).uid
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.delete(f"/regulartask/{rt_uid2}")
    assert r.status_code == 403
    db.expire_all()
    regulartask = await crud.regulartask.get(db, uid2, uid=rt_uid2)
    assert regulartask is not None
    compare(schemas.SRegularTaskCreate, regulartask, create)
