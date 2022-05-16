from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SMemorizeCardOut])
async def read_memorizecards(
    stack: Optional[int],
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Memorize Cards.
    """
    return await crud.memorizecard.get_multi(_db, _user.uid, stack=stack)


@router.get("/{uid}", response_model=schemas.SMemorizeCardOut, responses=resp.C34)
async def read_memorizecard_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Card.
    """
    return await crud.memorizecard.get(_db, _user.uid, uid=uid, r404=True)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_memorizecard(
    *,
    uid: int,
    card_in: schemas.SMemorizeCardUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Memorize Card.
    """
    await crud.memorizecard.update(_db, _user.uid, uid=uid, obj_in=card_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SMemorizeCardOut)
async def create_memorizecard(
    card_in: schemas.SMemorizeCardCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Memorize Card.
    """
    return await crud.memorizecard.create(_db, _user.uid, obj_in=card_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_memorizecard(
    *,
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Memorize Card.
    """
    await crud.memorizecard.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)
