from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SMemorizeStackOut])
async def read_memorizestacks(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Memorize Stacks.
    """
    return await crud.memorizestack.get_multi(_db, _user.uid)


@router.get("/statistics", response_model=list)
async def read_memorizestacks_statistics(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Stack Statistics.
    """
    return await crud.memorizestack.get_stat(_db, _user.uid)


@router.get("/{uid}", response_model=schemas.SMemorizeStackOut, responses=resp.C34)
async def read_memorizestack_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Stack.
    """
    return await crud.memorizestack.get(_db, _user.uid, uid=uid, r404=True)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_memorizestack(
    *,
    uid: int,
    memorizestack_in: schemas.SMemorizeStackUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Memorize Stack.
    """
    await crud.memorizestack.update(_db, _user.uid, uid=uid, obj_in=memorizestack_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SMemorizeStackOut)
async def create_memorizestack(
    stack_in: schemas.SMemorizeStackCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Memorize Stack.
    """
    return await crud.memorizestack.create(_db, _user.uid, obj_in=stack_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_memorizestack(
    *,
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Memorize Stack.
    """
    await crud.memorizestack.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)
