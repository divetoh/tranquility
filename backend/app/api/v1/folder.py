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