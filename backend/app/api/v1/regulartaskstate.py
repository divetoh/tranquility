from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp


router = APIRouter()


@router.get("/{statedate}", response_model=List[schemas.SRegularTaskStateOut])
async def read_regulartaskstate(
    statedate: date,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return RegularTaskState for date.
    """
    return await crud.regulartaskstate.get_multi(db, statedate=statedate, user=current_user.uid)


@router.get("/", response_model=List[schemas.SRegularTaskStateOut])
async def read_regulartaskstate_multi(
    start: date,
    end: date,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return RegularTaskState for date range.
    """
    return await crud.regulartaskstate.get_multi_bydate(db, start=start, end=end, user=current_user.uid)


@router.post("/", response_model=schemas.SRegularTaskStateOut)
async def create_regulartaskstate(
    *,
    regulartaskstate_in: schemas.SRegularTaskStateCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create RegularTaskState.
    """
    return await crud.regulartaskstate.create(db, obj_in=regulartaskstate_in, user=current_user.uid)


@router.delete("/{statedate}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_regulartaskstate(
    *,
    statedate: date,
    regulartask: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete RegularTaskState.
    """
    await crud.regulartaskstate.remove(
        db,
        user=current_user.uid,
        statedate=statedate,
        regulartask=regulartask,
        r404=True,
    )
    return schemas.SBoolOut(state=True)
