import uuid
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.SToken)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    _db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(_db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.uid, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post("/login/demo-token", response_model=schemas.SToken)
async def demo_access_token(
    _db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Generate demo user account.
    """
    if settings.DEMO_USERS == 0:
        raise HTTPException(
            status_code=403,
            detail="Demo mode disabled.",
        )
    # Check account count limit
    cnt = await crud.user.get_count(_db)
    if cnt >= settings.DEMO_USERS:
        raise HTTPException(
            status_code=507,
            detail="Maximum count of demo account reached. Try again later.",
        )
    # Create demo account
    tmpid = uuid.uuid4().hex
    temp_user = schemas.SUserCreate(email=tmpid + "@test.test", password=tmpid, full_name="Demo account")
    user = await crud.user.create(_db, obj_in=temp_user, data_source="demo.json")
    access_token_expires = timedelta(minutes=settings.DEMO_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.uid, expires_delta=access_token_expires),
        "token_type": "bearer",
    }
