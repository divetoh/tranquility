from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/{uid}", response_model=schemas.SFolderOut, responses=resp.C34)
async def read_folder_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Folder.
    """
    return await crud.folder.get(_db, _user.uid, uid=uid, r404=True)


@router.get("/", response_model=list[schemas.SFolderOut])
async def read_folder_multi(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Folders.
    """
    return await crud.folder.get_multi(_db, _user.uid)


@router.get("/{uid}/content", response_model=list[schemas.SFolderContent])
async def read_folder_content(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Folders.
    """
    return await crud.folder.get_content(_db, _user.uid, folder=uid)


@router.post("/", response_model=schemas.SFolderOut)
async def create_folder(
    *,
    folder_in: schemas.SFolderCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create Folder.
    """
    return await crud.folder.create(_db, _user.uid, obj_in=folder_in)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_folder(
    *,
    uid: int,
    folder_in: schemas.SFolderUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Folder.
    """
    await crud.folder.update(_db, _user.uid, uid=uid, obj_in=folder_in)
    return schemas.SBoolOut(state=True)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_folder(
    *,
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Folder.
    """
    await crud.folder.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)