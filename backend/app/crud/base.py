"""
Database access layer

* CRUDBase - object identified by uid value

Generic parameters:
* ModelType - SQLAlchemy Model class
* CreateSchemaType - pydantic schema for object creating request
* UpdateSchemaType - pydantic schema for object update request
"""

from typing import Any, Generic, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import MixinUID

ModelType = TypeVar("ModelType", bound=MixinUID)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Database access layer base class for object without owner field.

        Parameters:
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, *, uid: Any, r404: bool = False) -> Optional[ModelType]:
        """
        Get object from DB.

        Raise HTTPException:
        * 404 - if object absent, and `r404` parameter is True.
        """
        query = await db.scalars(select(self.model).filter(self.model.uid == uid))
        result = query.first()
        await db.commit()
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return result

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await db.scalars(select(self.model).offset(skip).limit(limit))
        await db.commit()
        return result.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        await db.commit()
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        uid: int,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * uid - object uid.
        * obj_in - Dict or pydantic update schema with new data.

        Raise HTTPException:
        * 404 - if object absent.
        """
        db_obj = await self.get(db, uid=uid)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Does not exist in the system")
        return await self.update_byobj(db, db_obj=db_obj, obj_in=obj_in)

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * db_obj - SQLAlchemy object selected from DB.
        * obj_in - Dict or pydantic update schema with new data.
        """
        if db_obj.update_bydict(obj_in) > 0:
            try:
                await db.flush()
                await db.refresh(db_obj)
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Non uniq parameter.",
                ) from None
        return db_obj

    async def remove(self, db: AsyncSession, *, uid: int, r404: bool = False) -> int:
        """
        Remove object from DB.
        Return deleted row count.

        Raise HTTPException:
        * 404 - if object absent, and `r404` parameter is True.
        """
        query = await db.execute(delete(self.model).where(self.model.uid == uid))
        await db.commit()
        result = query.rowcount     # type: ignore
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return result
