from datetime import date
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SMemorizeCategoryOut])
async def read_memorizecategorys(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Memorize Categorys.
    """
    return await crud.memorizecategory.get_multi(_db, _user.uid)


@router.get("/readycount/{dt}", response_model=dict[int, schemas.SMemorizeCardsReadyCount])
async def read_readycount(
    dt: date,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return count of Cards redy for answer for date. Grouped by category.
    """
    return await crud.memorizecategory.get_readycount(_db, _user.uid, dt)


@router.get("/{uid}", response_model=schemas.SMemorizeCategoryOut, responses=resp.C34)
async def read_memorizecategory_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Category.
    """
    return await crud.memorizecategory.get(_db, _user.uid, uid=uid, r404=True)


@router.get("/{uid}/cards", response_model=list[schemas.SMemorizeCardOut], responses=resp.C34)
async def read_memorizecards_by_category(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Cards by Category.
    """
    return await crud.memorizecard.get_by_category(_db, _user.uid, category=uid)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_memorizecategory(
    *,
    uid: int,
    category_in: schemas.SMemorizeCategoryUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Memorize Category.
    """
    await crud.memorizecategory.update(_db, _user.uid, uid=uid, obj_in=category_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SMemorizeCategoryOut)
async def create_memorizecategory(
    category_in: schemas.SMemorizeCategoryCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Memorize Category.
    """
    return await crud.memorizecategory.create(_db, _user.uid, obj_in=category_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_memorizecategory(
    *,
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Memorize Category.
    """
    await crud.memorizecategory.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)
