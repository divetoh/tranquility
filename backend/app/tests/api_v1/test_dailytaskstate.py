from datetime import date
from httpx import AsyncClient
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.main import app
from app.tests.utils.daily import cr_rand_dailytask, cr_rand_dailytasks, cr_rand_dailytaskstates
from app.tests.utils.users import cr_rand_user, user_token
from app.tests.utils.utils import BURL, compare


@pytest.mark.anyio
async def test_dailytaskstate_get(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dt = await cr_rand_dailytasks(db, uid, 3)
    dts = await cr_rand_dailytaskstates(db, (dt[0]["uid"], dt[1]["uid"]), (date(2022, 1, 1),))
    await cr_rand_dailytaskstates(db, (dt[1]["uid"], dt[2]["uid"]), (date(2022, 1, 2),))

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/dailytaskstate/2022-01-01")
    assert r.status_code == 200
    web_res = r.json()
    assert len(web_res) == 2
    web_res.sort(key=lambda x: x["dailytask"])
    compare(schemas.SDailyTaskStateOut, web_res[0], dts[0])
    compare(schemas.SDailyTaskStateOut, web_res[1], dts[1])


@pytest.mark.anyio
async def test_dailytaskstate_get_and_create(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dt = await cr_rand_dailytasks(db, uid, 3, is_active=(True, True, False))

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/dailytaskstate/2022-01-01")
    assert r.status_code == 200
    web_res = r.json()
    assert len(web_res) == 2
    web_res.sort(key=lambda x: x["dailytask"])
    db.expire_all()
    db_dts = await crud.dailytaskstate.get_multi(db, uid, statedate=date(2022, 1, 1))
    db_dts.sort(key=lambda x: x.dailytask)
    compare(schemas.SDailyTaskStateOut, web_res[0], db_dts[0])
    compare(schemas.SDailyTaskStateOut, web_res[1], db_dts[1])
    assert web_res[0]["dailytask"] == dt[0]["uid"]
    assert web_res[1]["dailytask"] == dt[1]["uid"]


@pytest.mark.anyio
async def test_dailytaskstate_get_multi(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dt = await cr_rand_dailytask(db, uid)
    dates = (date(2022, 1, 1), date(2022, 1, 2), date(2022, 1, 4), date(2022, 1, 5))
    dts = await cr_rand_dailytaskstates(db, (dt["uid"],), dates)

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/dailytaskstate/", params={"start": "2022-01-02", "end": "2022-01-04"})
    assert r.status_code == 200
    web_res = r.json()
    assert len(web_res) == 2
    web_res.sort(key=lambda x: x["statedate"])
    compare(schemas.SDailyTaskStateOut, web_res[0], dts[1])
    compare(schemas.SDailyTaskStateOut, web_res[1], dts[2])


@pytest.mark.anyio
async def test_dailytaskstate_update(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    dt = await cr_rand_dailytask(db, uid)
    dts = await cr_rand_dailytaskstates(db, (dt["uid"],), (date(2022, 1, 1),))

    update = {"state": (dts[0]["state"] + 1) % 3}
    # Correct update
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put("/dailytaskstate/2022-01-01", json=update, params={"dailytask": dt["uid"]})
    assert r.status_code == 200
    assert r.json()["state"]
    db.expire_all()
    db_dts = await crud.dailytaskstate.get(db, uid, dailytask=dt["uid"], statedate=date(2022, 1, 1))
    assert db_dts is not None
    compare(schemas.SDailyTaskStateUpdate, db_dts, update)

    # Update non-existent record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put("/dailytaskstate/2022-01-01", json=update, params={"dailytask": dt["uid"] + 1})
    assert r.status_code == 404

    # Update other user record
    uid2 = (await cr_rand_user(db)).uid
    dt2 = await cr_rand_dailytask(db, uid2)
    dts2 = await cr_rand_dailytaskstates(db, (dt2["uid"],), (date(2022, 1, 1),))

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put("/dailytaskstate/2022-01-01", json=update, params={"dailytask": dt2["uid"]})
    assert r.status_code == 404
    db.expire_all()
    dailytask = await crud.dailytaskstate.get(db, user=uid2, dailytask=dt2["uid"], statedate=date(2022, 1, 1))
    assert dailytask is not None
    compare(schemas.SDailyTaskStateUpdate, dailytask, dts2[0])
