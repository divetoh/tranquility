from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.importdata import import_data
from app.models.user import User
from app.schemas.user import SUserCreate, SUserUpdate


class CRUDUser(CRUDBase[User, SUserCreate, SUserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Get user by e-mail.
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count(User.uid)))
        return result.scalar_one()

    async def get_demo_users(self, db: AsyncSession) -> list[User]:
        """
        Get demo users with expired time
        """
        if settings.DEMO_USERS == 0:
            return []
        result = await db.execute(select(User).filter(
            User.is_superuser == 0,
            User.email.like("%@test.test"),
            User.created_dt < datetime.now() - timedelta(minutes=settings.DEMO_ACCESS_TOKEN_EXPIRE_MINUTES),
        ))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: SUserCreate, data_source: Optional[str] = "init.json") -> User:
        """
        Create new user.
        """
        if data_source not in ["init.json", "demo.json"]:
            data_source = "init.json"
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            coreactivity=None,
            coretasklist=None,
        )
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="The user with this email already exists in the system.",
            ) from None
        # Generate starter content
        if data_source is None:
            return db_obj
        return await import_data(db, db_obj, data_source)

    async def update_byobj(self, db: AsyncSession, db_obj: User, *, obj_in: Union[SUserUpdate, dict[str, Any]]) -> User:
        """
        Update user record.
        If updating password - make hashed_password
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update_byobj(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password, return user object or None.
        """
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
