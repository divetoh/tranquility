from typing import Any, Optional, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app import schemas
from app.models import MemorizeCard, MemorizeCategory, MemorizeStack
from .crud_category import memorizecategory
from .crud_stack import memorizestack


class CRUDMemorizeCard():
    async def get_multi(
        self,
        db: AsyncSession,
        user: int,
        *,
        skip: int = 0,
        limit: int = 100,
        stack: Optional[int] = None,
    ) -> list[MemorizeCard]:
        query = select(MemorizeCard).join(MemorizeCard.stack_r).\
            outerjoin(MemorizeCard.state_r).options(contains_eager('state_r'))
        if stack is not None:
            query = query.filter(MemorizeCard.stack == stack)
        result = await db.execute(query.filter(MemorizeStack.user == user).offset(skip).limit(limit))
        return result.unique().scalars().all()

    async def get(self, db: AsyncSession, user: int, *, uid: Any, r404: bool = False) -> Optional[MemorizeCard]:
        """
        Get object from DB.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent, and `r404` parameter is True.
        """
        query = select(MemorizeCard).join(MemorizeStack).outerjoin(MemorizeCard.state_r).\
            options(contains_eager('state_r').contains_eager('stack_r')).filter(MemorizeCard.uid == uid)
        result = (await db.execute(query)).unique().scalars().first()
        if result and result.stack_r.user != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return result

    async def remove(
        self,
        db: AsyncSession,
        user: int,
        *,
        uid: int,
        r404: bool = False,
    ) -> int:
        """
        Remove object from DB.
        Return deleted row count.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent, and `r404` parameter is True.
        """
        query = select(MemorizeStack.user).join(MemorizeCard).filter(MemorizeCard.uid == uid)
        result = (await db.execute(query)).scalars().first()
        if not result and r404:
            raise HTTPException(status_code=404, detail="Object not found.")
        elif not result:
            return 0
        elif result != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        query2 = await db.execute(delete(MemorizeCard).where(MemorizeCard.uid == uid))
        await db.commit()
        result = query2.rowcount     # type: ignore
        return int(result)

    async def create(self, db: AsyncSession, user: int, *, obj_in: schemas.SMemorizeCardCreate) -> MemorizeCard:
        # Check stack access rights
        await memorizestack.check_access(db, user, uid=obj_in.stack)

        # Check category access rights
        if obj_in.category is not None:
            query2 = select(MemorizeCategory.user).filter(MemorizeCategory.uid == obj_in.category)
            result2 = (await db.execute(query2)).scalars().first()
            if not result2:
                raise HTTPException(status_code=404, detail="Object not found.")
            elif result2 != user:
                raise HTTPException(status_code=403, detail="Access denied.")

        # Create Card
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = MemorizeCard(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        user: int,
        *,
        uid: int,
        obj_in: Union[schemas.SMemorizeCardUpdate, dict[str, Any]],
    ) -> MemorizeCard:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * uid - object uid.
        * obj_in - Dict or pydantic update schema with new data.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent.
        """
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)

        # Check current Card existence and access rights
        query = select(MemorizeCard).join(MemorizeStack).options(selectinload(MemorizeCard.stack_r)).\
            filter(MemorizeCard.uid == uid)
        db_obj = (await db.execute(query)).scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found.")
        elif db_obj.stack_r.user != user:
            raise HTTPException(status_code=403, detail="Access denied.")

        # Check updated Category existence and access rights
        if "category" in obj_in:
            await memorizecategory.check_access(db, user, uid=obj_in["category"])

        # Check updated Stack existence and access rights
        if "stack" in obj_in:
            await memorizestack.check_access(db, user, uid=obj_in["stack"])

        return await self.update_byobj(db, db_obj=db_obj, obj_in=obj_in)

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: MemorizeCard,
        obj_in: Union[schemas.SMemorizeCardUpdate, dict[str, Any]],
    ) -> MemorizeCard:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * db_obj - SQLAlchemy object selected from DB.
        * obj_in - Dict or pydantic update schema with new data.

        Method don't check owner and don't rise exception.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


memorizecard = CRUDMemorizeCard()
