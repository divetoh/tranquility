from datetime import date
import pytest  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.tests.utils.utils import compare


@pytest.mark.anyio
async def test_daystate_get(db: AsyncSession, reguser: models.User) -> None:
    uid = reguser.uid
    daystate = schemas.SDayStateCreate(
        statedate=date(2022, 1, 1),
        description="Test daystate get",
        rating=5,
        complited="[1,2,3]",
    )
    await crud.daystate.create(db, uid, obj_in=daystate)
    db.expire_all()
    dbdaystate = await crud.daystate.get(db, uid, statedate=daystate.statedate)
    assert dbdaystate is not None
    assert dbdaystate.user == uid
    compare(schemas.SDayStateCreate, dbdaystate, daystate)
    # Reading non-existent record
    dbdaystate2 = await crud.daystate.get(db, uid, statedate=date(2022, 1, 2))
    assert dbdaystate2 is None


@pytest.mark.anyio
async def test_daystate_get_multi_bydate(db: AsyncSession, reguser: models.User) -> None:
    uid = reguser.uid
    startdate = date(2022, 1, 1)
    daystate = schemas.SDayStateCreate(
        statedate=startdate,
        description="test",
        rating=5,
        complited="[1,2,3]",
    )
    await crud.daystate.create(db, uid, obj_in=daystate)
    daystate.statedate = date(2022, 1, 2)
    await crud.daystate.create(db, uid, obj_in=daystate)
    daystate.statedate = date(2022, 1, 3)
    await crud.daystate.create(db, uid, obj_in=daystate)
    daystate.statedate = date(2022, 1, 4)
    await crud.daystate.create(db, uid, obj_in=daystate)
    db.expire_all()
    result = await crud.daystate.get_multi_bydate(db, uid, start=date(2022, 1, 2), end=date(2022, 1, 3))
    assert len(result) == 2
    assert all(result)
    assert {x.statedate for x in result} == {date(2022, 1, 3), date(2022, 1, 2)}


@pytest.mark.anyio
async def test_daystate_create(db: AsyncSession, reguser: models.User) -> None:
    uid = reguser.uid
    daystate = schemas.SDayStateCreate(
        statedate=date(2022, 1, 2),
        description="test",
        rating=5,
        complited="[1,2,3]",
    )
    await crud.daystate.create(db, uid, obj_in=daystate)
    db.expire_all()
    dbdaystate = await crud.daystate.get(db, uid, statedate=daystate.statedate)
    assert dbdaystate is not None
    assert dbdaystate.user == uid
    compare(schemas.SDayStateCreate, dbdaystate, daystate)
    # Try create record with same date
    dbdaystate2 = await crud.daystate.create(db, uid, obj_in=daystate)
    assert dbdaystate2 is None


@pytest.mark.anyio
async def test_daystate_update_byobj(db: AsyncSession, reguser: models.User) -> None:
    uid = reguser.uid
    daystate = schemas.SDayStateCreate(
        statedate=date(2022, 1, 2),
        description="test",
        rating=5,
        complited="[1,2,3]",
    )
    dbdaystate = await crud.daystate.create(db, uid, obj_in=daystate)
    assert dbdaystate is not None

    # Update by SDayStateUpdate
    update1 = schemas.SDayStateUpdate(description="test2", rating=1, complited="[4,5,6]")
    await crud.daystate.update_byobj(db, db_obj=dbdaystate, obj_in=update1)
    db.expire_all()
    dbdaystate2 = await crud.daystate.get(db, uid, statedate=daystate.statedate)
    assert dbdaystate2 is not None
    compare(schemas.SDayStateUpdate, dbdaystate2, update1)

    # Update by dict
    update2 = {"description": "test3", "rating": 3, "complited": "[7,8,9]"}
    await crud.daystate.update_byobj(db, db_obj=dbdaystate, obj_in=update2)
    db.expire_all()
    dbdaystate3 = await crud.daystate.get(db, uid, statedate=daystate.statedate)
    assert dbdaystate3 is not None
    compare(schemas.SDayStateUpdate, dbdaystate3, update2)
