from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp


router = APIRouter()


@router.get("/", response_model=List[schemas.SRegularTaskOut])
async def read_regulartask(
    skip: int = 0,
    limit: int = 1000,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all RegularTask list, sliced by skip/limit.
    """
    regulartasks = await crud.regulartask.get_multi(_db, _user.uid, skip=skip, limit=limit)
    return regulartasks


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_regulartask(
    uid: int,
    regulartask_in: schemas.SRegularTaskUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update RegularTask.
    """
    await crud.regulartask.update(_db, _user.uid, uid=uid, obj_in=regulartask_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SRegularTaskOut)
async def create_regulartask(
    regulartask_in: schemas.SRegularTaskCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new RegularTask.
    """
    return await crud.regulartask.create(_db, _user.uid, obj_in=regulartask_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_regulartask_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete RegularTask and all associated RegularTaskState.
    """
    await crud.regulartask.remove(_db, _user.uid, uid=uid, r404=True)
    return schemas.SBoolOut(state=True)
