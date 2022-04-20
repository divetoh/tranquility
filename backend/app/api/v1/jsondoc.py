from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/{uid}", response_model=schemas.SJSONDocOut, responses=resp.C34)
async def read_jsondoc_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return JSONDoc.
    """
    return await crud.jsondoc.get(_db, _user.uid, uid=uid, r404=True)


@router.get("/", response_model=list[schemas.SJSONDocOut])
async def read_jsondoc_multi(
    doctype: str,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all JSONDocs, filtered by doctype.
    """
    return await crud.jsondoc.get_bydoctype(_db, _user.uid, doctype=doctype)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_jsondoc(
    *,
    uid: int,
    jsondoc_in: schemas.SJSONDocUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update JSONDoc.
    """
    await crud.jsondoc.update(_db, _user.uid, uid=uid, obj_in=jsondoc_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SJSONDocOut)
async def create_jsondoc(
    *,
    jsondoc_in: schemas.SJSONDocCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create JSONDoc.
    """
    return await crud.jsondoc.create(_db, _user.uid, obj_in=jsondoc_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34 | resp.C9DEL)
async def delete_jsondoc_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete JSONDoc.
    """
    if uid in (_user.coreactivity, _user.coretasklist):
        raise HTTPException(status_code=409, detail="Can't delete core object.")
    await crud.jsondoc.remove(_db, _user.uid, uid=uid, r404=True)
    return schemas.SBoolOut(state=True)
