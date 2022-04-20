from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SUser])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users. Superuser method.
    """
    return await crud.user.get_multi(_db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.SUser, responses=resp.C9UID)
async def create_user(
    user_in: schemas.SUserCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user. Superuser method.
    """
    user = await crud.user.get_by_email(_db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system.",
        )
    return await crud.user.create(_db, obj_in=user_in)


@router.put("/me", response_model=schemas.SUser)
async def update_user_me(
    password: str = Body(None),
    full_name: str = Body(None),
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user_in = schemas.SUserUpdate(**jsonable_encoder(_user))
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    user = await crud.user.update_byobj(_db, db_obj=_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.SUser)
def read_user_me(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return _user


@router.get("/{user_id}", response_model=schemas.SUser, responses=resp.C3)
async def read_user_by_id(
    user_id: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific user by id. Only own profile avaliable for not superuser.
    """
    if user_id == _user.uid:
        return _user
    if not _user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return await crud.user.get(_db, uid=user_id)


@router.put("/{user_id}", response_model=schemas.SUser, responses=resp.C34 | resp.C9UID)
async def update_user(
    user_id: int,
    user_in: schemas.SUserAdminUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user. Superuser method.
    """
    if user_in.email is not None:
        user = await crud.user.get_by_email(_db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=409,
                detail="The user with this email already exists in the system.",
            )
    return await crud.user.update(_db, uid=user_id, obj_in=user_in)
