from datetime import date
from httpx import AsyncClient
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.main import app
from app.tests.utils.users import user_token
from app.tests.utils.utils import BURL, compare


@pytest.mark.anyio
async def test_daystate_get(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    daystate = schemas.SDayStateCreate(
        statedate=date(2022, 1, 1),
        description="Test daystate",
        rating=5,
        complited="[1,2,3]",
    )
    await crud.daystate.create(db, uid, obj_in=daystate)

    # Correct request
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get(f"/daystate/{daystate.statedate}")
    assert r.status_code == 200
    web_daystate = r.json()
    compare(schemas.SDayStateOut, web_daystate, daystate)

    # Create new daystate if it's doesn't exist
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get(f"/daystate/{date(2022, 1, 2)}")
    assert r.status_code == 200
    web_daystate = r.json()
    daystate2 = await crud.daystate.get(db, uid, statedate=date(2022, 1, 2))
    assert daystate2 is not None
    compare(schemas.SDayStateOut, web_daystate, daystate2)


@pytest.mark.anyio
async def test_daystate_get_multi(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    daystate = schemas.SDayStateCreate(
        statedate=date(2022, 1, 1),
        description="Test daystate",
        rating=5,
        complited="[1,2,3]",
    )
    daystate2 = daystate.copy(update={"statedate": date(2022, 1, 2)})
    daystate3 = daystate.copy(update={"statedate": date(2022, 1, 3)})
    daystate4 = daystate.copy(update={"statedate": date(2022, 1, 4)})
    await crud.daystate.create(db, uid, obj_in=daystate)
    await crud.daystate.create(db, uid, obj_in=daystate2)
    await crud.daystate.create(db, uid, obj_in=daystate3)
    await crud.daystate.create(db, uid, obj_in=daystate4)

    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.get("/daystate/", params={"start": str(daystate2.statedate), "end": str(daystate3.statedate)})
    assert r.status_code == 200
    web_daystate = r.json()
    assert len(web_daystate) == 2
    web_daystate.sort(key=lambda x: x["statedate"])
    compare(schemas.SDayStateOut, web_daystate[0], daystate2)
    compare(schemas.SDayStateOut, web_daystate[1], daystate3)


@pytest.mark.anyio
async def test_daystate_update(db: AsyncSession, reguser: models.User) -> None:
    uid, token = reguser.uid, user_token(reguser)
    create = {
        "description": "Create record",
        "rating": 5,
        "complited": "[1,2,3]",
    }
    # First Update will create new record
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put("/daystate/2022-01-01", json=create)
    assert r.status_code == 200
    assert r.json()["state"]
    daystate = await crud.daystate.get(db, uid, statedate=date(2022, 1, 1))
    assert daystate is not None
    compare(schemas.SDayStateOut, daystate, create | {"statedate": "2022-01-01"})
    # Test partial update
    db.expire_all()
    update = {
        "description": "Update record",
        "rating": 4,
    }
    async with AsyncClient(app=app, base_url=BURL, headers=token) as ac:
        r = await ac.put("/daystate/2022-01-01", json=update)
    assert r.json()["state"]
    daystate = await crud.daystate.get(db, uid, statedate=date(2022, 1, 1))
    assert daystate is not None
    compare(schemas.SDayStateOut, daystate.as_dict(), create | update | {"statedate": "2022-01-01"})
