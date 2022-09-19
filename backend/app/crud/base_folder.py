"""
Database access layer

* CRUDBaseFolder - object identified by uid, and check owner by folder rights

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
from sqlalchemy.orm import joinedload

from app.db.base_class import MixinFolder
from app.models import Folder


AuthModelType = TypeVar("AuthModelType", bound=MixinFolder)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBaseFolder(Generic[AuthModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[AuthModelType]):
        """
        Database access layer base class for object with folder field.

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
        query = select(self.model).options(joinedload(self.model.folder_r).load_only("user")).filter(self.model.uid == uid)
        result = await db.scalars(query)
        await db.commit()
        model = result.first()
        if model and model.folder_r.user != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        if r404 and not model:
            raise HTTPException(status_code=404, detail="Object not found.")
        return model

    async def check_access(self, db: AsyncSession, user: int, *, uid: Any) -> None:
        """
        Check object existance, and owner user.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent.
        """
        res = await db.scalars(select(Folder.user).join(self.model).filter(self.model.uid == uid))
        uuid = res.first()
        if uuid is None:
            raise HTTPException(status_code=404, detail="Object absent.")
        if uuid != user:
            raise HTTPException(status_code=403, detail="Access denied.")

    async def check_folder_access(self, db: AsyncSession, user: int, *, uid: Any) -> None:
        """
        Folder existance, and owner user.

        Raise HTTPException:
        * 403 - if user not own object.
        * 404 - if object absent.
        """
        res = await db.scalars(select(Folder.user).filter(Folder.uid == uid))
        uuid = res.first()
        if uuid is None:
            raise HTTPException(status_code=404, detail="Folder absent.")
        if uuid != user:
            raise HTTPException(status_code=403, detail="Access denied.")

    async def get_multi(self, db: AsyncSession, user: int, *, skip: int = 0, limit: int = 100) -> list[AuthModelType]:
        """
        Get objects from DB. Skip, limit - for slicing query result.

        Method don't rise 403 exception, but return only objects owned by user.
        """
        query = select(self.model).join(Folder).filter(Folder.user == user).offset(skip).limit(limit)
        result = await db.scalars(query)
        await db.commit()
        return result.all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: CreateSchemaType) -> AuthModelType:
        obj_in_data = obj_in.dict()
        self.check_folder_access(db, user, uid = obj_in_data["folder"])
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        await db.commit()
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
        res = await db.scalars(select(Folder.user).join(self.model).filter(self.model.uid == uid))
        uuid = res.first()
        if not uuid and r404:
            raise HTTPException(status_code=404, detail="Object not found.")
        elif not uuid:
            return 0
        elif uuid != user:
            raise HTTPException(status_code=403, detail="Access denied.")
        query = await db.execute(delete(self.model).where(self.model.uid == uid))
        await db.commit()
        result = query.rowcount     # type: ignore
        return int(result)
