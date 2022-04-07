from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/{uid}", response_model=schemas.SMarkdownOut, responses=resp.C34)
async def read_markdown_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Markdown.
    """
    return await crud.markdown.get(_db, _user.uid, uid=uid, r404=True)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_markdown(
    *,
    uid: int,
    markdown_in: schemas.SMarkdownUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Markdown.
    """
    await crud.markdown.update(_db, _user.uid, uid=uid, obj_in=markdown_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SMarkdownOut)
async def create_markdown(
    *,
    markdown_in: schemas.SMarkdownCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create Markdown.
    """
    return await crud.markdown.create(_db, _user.uid, obj_in=markdown_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_markdown(
    *,
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Markdown.
    """
    await crud.markdown.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)
