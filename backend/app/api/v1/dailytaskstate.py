from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/{statedate}", response_model=List[schemas.SDailyTaskStateOut])
async def read_dailytaskstate(
    statedate: date,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return DailyTaskStates on date. Creates DailyTaskStates if they are absent.
    """
    dailytaskstates = await crud.dailytaskstate.get_multi(_db, _user.uid, statedate=statedate)
    if len(dailytaskstates) != 0:
        return dailytaskstates
    # TODO: Create all states with one query
    result = []
    dailytasks = await crud.dailytask.get_multi(_db, _user.uid, skip=0, limit=1000)
    for dt in dailytasks:
        if dt.is_active:
            dts = schemas.SDailyTaskStateOut(statedate=statedate, dailytask=dt.uid, state=0)
            result.append(await crud.dailytaskstate.create(_db, _user.uid, obj_in=dts))
    return result


@router.get("/", response_model=List[schemas.SDailyTaskStateOut])
async def read_dailytaskstate_multi(
    start: date,
    end: date,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return DailyTaskStates for date range.
    """
    dailytaskstate = await crud.dailytaskstate.get_multi_bydate(_db, _user.uid, start=start, end=end)
    return dailytaskstate


@router.put("/{statedate}", response_model=schemas.SBoolOut, responses=resp.C4)
async def update_dailytaskstate(
    statedate: date,
    dailytask: int,
    dailytaskstate_in: schemas.SDailyTaskStateUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update DailyTaskState.
    """
    dailytaskstate = await crud.dailytaskstate.get(_db, _user.uid, statedate=statedate, dailytask=dailytask)
    if not dailytaskstate:
        raise HTTPException(status_code=404, detail="DailyTaskState not found")
    dailytaskstate = await crud.dailytaskstate.update_byobj(_db, db_obj=dailytaskstate, obj_in=dailytaskstate_in)
    return schemas.SBoolOut(state=True)
