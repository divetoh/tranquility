from datetime import date

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RegularTask, RegularTaskState
from app.schemas.regulartaskstate import SRegularTaskStateCreate, SRegularTaskStateOut
from .crud_regulartask import regulartask as crud_regulartask


class CRUDRegularTaskState():
    async def get_multi(self, db: AsyncSession, user: int, *, statedate: date) -> list[SRegularTaskStateOut]:
        query = select(RegularTaskState).join(RegularTask).filter(
            RegularTask.user == user,
            RegularTaskState.statedate == statedate,
        )
        return (await db.execute(query)).scalars().all()

    async def get_multi_bydate(
        self,
        db: AsyncSession,
        user: int,
        *,
        start: date,
        end: date,
    ) -> list[SRegularTaskStateOut]:
        """ Return all user's RegularTaskState for date in range. """
        query = select(RegularTaskState).join(RegularTask).filter(
            RegularTask.user == user,
            RegularTaskState.statedate >= start,
            RegularTaskState.statedate <= end,
        )
        return (await db.execute(query)).scalars().all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: SRegularTaskStateCreate) -> RegularTaskState:
        await crud_regulartask.check_access(db, user, uid=obj_in.regulartask)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = RegularTaskState(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db: AsyncSession,
        user: int,
        *,
        statedate: date,
        regulartask: int,
        r404: bool = False,
    ) -> int:
        await crud_regulartask.check_access(db, user, uid=regulartask)
        query = await db.execute(delete(RegularTaskState).where(
            RegularTaskState.statedate == statedate,
            RegularTaskState.regulartask == regulartask,
        ))
        await db.commit()
        result = query.rowcount     # type: ignore
        if r404 and not result:
            raise HTTPException(status_code=404, detail="Object not found.")
        return int(result)


regulartaskstate = CRUDRegularTaskState()
