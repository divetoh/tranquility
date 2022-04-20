from datetime import date
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{statedate}", response_model=schemas.SDayStateOut)
async def read_daystate(
    statedate: date,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return DayState. Create DayState, if absent.
    """
    daystate = await crud.daystate.get(_db, _user.uid, statedate=statedate)
    if daystate is None:
        # Create day state if it absent
        newdaystate = schemas.SDayStateCreate(statedate=statedate)
        daystate = await crud.daystate.create(_db, _user.uid, obj_in=newdaystate)
    return daystate


@router.get("/", response_model=list[schemas.SDayStateOut])
async def read_daystate_multi(
    start: date,
    end: date,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return DayStates for date range.
    """
    daystate = await crud.daystate.get_multi_bydate(_db, _user.uid, start=start, end=end)
    return daystate


@router.put("/{statedate}", response_model=schemas.SBoolOut)
async def update_daystate(
    statedate: date,
    daystate_in: schemas.SDayStateUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update DayState. Create DayState, if absent.
    """
    daystate = await crud.daystate.get(_db, _user.uid, statedate=statedate)
    if not daystate:
        # Create day state if it absent
        newdaystate = schemas.SDayStateCreate(statedate=statedate)
        daystate = await crud.daystate.create(_db, _user.uid, obj_in=newdaystate)

    daystate = await crud.daystate.update_byobj(_db, db_obj=daystate, obj_in=daystate_in)
    return schemas.SBoolOut(state=True)
