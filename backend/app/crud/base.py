"""
Base CRUD objects.

Object contains basic CRUD methods: Create, Read, Update, Delete

* CRUDBase - object identified by uid value
* CRUDBaseAuth - object identified by uid, and check owner by user value

Generic parameters:
* ModelType - SQLAlchemy Model class
* CreateSchemaType - pydantic schema for object creating request
* UpdateSchemaType - pydantic schema for object update request
"""

from typing import Any, Generic, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import MixinUID, MixinUser

ModelType = TypeVar("ModelType", bound=MixinUID)
AuthModelType = TypeVar("AuthModelType", bound=MixinUser)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD base class for object without user (owner) field.

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
        query = await db.execute(select(self.model).filter(self.model.uid == uid))
        result = query.scalars().first()
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return result

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
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
                await db.commit()
                await db.refresh(db_obj)
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


class CRUDBaseAuth(Generic[AuthModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[AuthModelType]):
        """
        CRUD base class for object with user (owner) field.

        Parameters:
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, user: int, *, uid: Any, r404: bool = False) -> Optional[AuthModelType]:
        """
        Get object from DB.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent, and `r404` parameter is True.
        """
        query = await db.execute(select(self.model).filter(self.model.uid == uid))
        result = query.scalars().first()
        if result and result.user != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return result

    async def check_access(self, db: AsyncSession, user: int, *, uid: Any) -> None:
        """
        Check object existance, and owner user.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent.
        """
        query = await db.execute(select(self.model.user).filter(self.model.uid == uid))
        result = query.scalars().first()
        if result is None:
            raise HTTPException(status_code=404, detail="Object absent.")
        if result != user:
            raise HTTPException(status_code=403, detail="Access denied.")

    async def get_multi(self, db: AsyncSession, user: int, *, skip: int = 0, limit: int = 100) -> list[AuthModelType]:
        """
        Get objects from DB. Skip, limit - for slicing query result.

        Method don't rise 403 exception, but return only objects owned by user.
        """
        result = await db.execute(select(self.model).filter(self.model.user == user).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: CreateSchemaType) -> AuthModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["user"] = user
        db_obj = self.model(**obj_in_data)
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
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> AuthModelType:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * uid - object uid.
        * obj_in - Dict or pydantic update schema with new data.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent.
        """
        db_obj = await self.get(db, user, uid=uid)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Does not exist in the system")
        return await self.update_byobj(db, db_obj=db_obj, obj_in=obj_in)

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: AuthModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> AuthModelType:
        """
        Update object in DB. Only filled fields will be updated.

        Parameters:
        * db_obj - SQLAlchemy object selected from DB.
        * obj_in - Dict or pydantic update schema with new data.

        Method don't check owner and don't rise exception.
        """
        if db_obj.update_bydict(obj_in) > 0:
            try:
                await db.commit()
                await db.refresh(db_obj)
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Non uniq parameter.",
                ) from None
        return db_obj

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
        query = await db.execute(select(self.model.user).filter(self.model.uid == uid))
        result = query.scalars().first()
        if not result and r404:
            raise HTTPException(status_code=404, detail="Object not found.")
        elif not result:
            return 0
        elif result != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        query = await db.execute(delete(self.model).where(self.model.uid == uid, self.model.user == user))
        await db.commit()
        result = query.rowcount     # type: ignore
        return int(result)
