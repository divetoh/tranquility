from datetime import date
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SDailyTaskOut])
async def read_dailytask(
    skip: int = 0,
    limit: int = 1000,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all DailyTask list, sliced by skip/limit.
    """
    dailytasks = await crud.dailytask.get_multi(_db, _user.uid, skip=skip, limit=limit)
    return dailytasks


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_dailytask(
    uid: int,
    dailytask_in: schemas.SDailyTaskUpdate,
    operationdate: Optional[date] = None,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update DailyTask. Create/delete DailyTaskState if needed (when is_active changes).
    """
    db_obj = await crud.dailytask.get(_db, _user.uid, uid=uid)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Does not exist in the system")

    if dailytask_in.is_active is not None and db_obj.is_active != dailytask_in.is_active:
        if operationdate is None:
            operationdate = date.today()
        if dailytask_in.is_active:
            await crud.dailytaskstate.create_chain(_db, _user.uid, fromdate=operationdate, dailytask=uid)
        else:
            await crud.dailytaskstate.remove_chain(_db, _user.uid, fromdate=operationdate, dailytask=uid)
    await crud.dailytask.update_byobj(_db, db_obj=db_obj, obj_in=dailytask_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SDailyTaskOut)
async def create_dailytask(
    dailytask_in: schemas.SDailyTaskCreate,
    operationdate: Optional[date] = None,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new DailyTask and generate DailyTaskState if needed.
    """
    dailytask = await crud.dailytask.create(_db, _user.uid, obj_in=dailytask_in)
    if dailytask.is_active:
        if operationdate is None:
            operationdate = date.today()
        await crud.dailytaskstate.create_chain(_db, _user.uid, fromdate=operationdate, dailytask=dailytask.uid)
    return dailytask


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_dailytask_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete DailyTask and all associated DailyTaskState.
    """
    await crud.dailytask.remove(_db, _user.uid, uid=uid, r404=True)
    return schemas.SBoolOut(state=True)
