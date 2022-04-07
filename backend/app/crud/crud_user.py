from typing import Any, Dict, Optional, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.jsondoc import SJSONDocCreate
from app.schemas.user import SUserCreate, SUserUpdate
from .crud_jsondoc import jsondoc


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

    async def create(self, db: AsyncSession, *, obj_in: SUserCreate) -> User:
        """
        Create new user.
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            coreactivity=None,
            coretasklist=None,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        # Generating empty activity and tasklist and assign they to user
        obj_tl = SJSONDocCreate(doctype="tasklist", name="Core Tasklist", jsondoc="[]")
        tasklist = await jsondoc.create(db=db, user=db_obj.uid, obj_in=obj_tl)
        obj_act = SJSONDocCreate(
            doctype="activity",
            name="Core Activity",
            jsondoc='{"name":"coreactivity","workspaces":[]}',
        )
        activity = await jsondoc.create(db=db, obj_in=obj_act, user=db_obj.uid)
        obj_upd = {"coreactivity": activity.uid, "coretasklist": tasklist.uid}
        return await self.update_byobj(db=db, db_obj=db_obj, obj_in=obj_upd)

    async def update_byobj(self, db: AsyncSession, db_obj: User, *, obj_in: Union[SUserUpdate, Dict[str, Any]]) -> User:
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
