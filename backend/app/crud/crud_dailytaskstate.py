from datetime import date
from typing import Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DailyTask, DailyTaskState
from app.schemas.dailytaskstate import SDailyTaskStateOut, SDailyTaskStateUpdate
from .crud_dailytask import dailytask as crud_dailytask


class CRUDDailyTaskState():
    async def get(self, db: AsyncSession, user: int, *, statedate: date, dailytask: int) -> Optional[DailyTaskState]:
        query = select(DailyTaskState).join(DailyTask).filter(
            DailyTask.user == user,
            DailyTaskState.statedate == statedate,
            DailyTaskState.dailytask == dailytask,
        )
        return (await db.execute(query)).scalars().first()

    async def get_multi(self, db: AsyncSession, user: int, *, statedate: date) -> list[DailyTaskState]:
        query = select(DailyTaskState).join(DailyTask).filter(
            DailyTask.user == user,
            DailyTaskState.statedate == statedate,
        )
        return (await db.execute(query)).scalars().all()

    async def get_multi_bydate(
        self,
        db: AsyncSession,
        user: int,
        *,
        start: date,
        end: date,
    ) -> list[DailyTaskState]:
        """ Return all user's DailyTaskState for date in range. """
        query = select(DailyTaskState).join(DailyTask).filter(
            DailyTask.user == user,
            DailyTaskState.statedate >= start,
            DailyTaskState.statedate <= end,
        )
        return (await db.execute(query)).scalars().all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: SDailyTaskStateOut) -> DailyTaskState:
        await crud_dailytask.check_access(db, user, uid=obj_in.dailytask)
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = DailyTaskState(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: DailyTaskState,
        obj_in: Union[SDailyTaskStateUpdate, dict[str, Any]],
    ) -> DailyTaskState:
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

    async def create_chain(self, db: AsyncSession, user: int, *, fromdate: date, dailytask: int) -> None:
        """
        Called after creation/enabling dailytask.
        Search all days>=`fromdate`, which allready have status for any dailytask,
        and add status for `dailytask` to this day.
        """
        # TODO: check "group by" in ORM?
        query = select(DailyTaskState.statedate).join(DailyTask).filter(
            DailyTask.user == user,
            DailyTaskState.statedate >= fromdate,
        )
        result = (await db.execute(query)).scalars().all()
        dates = set([x for x in result])
        for dt in dates:
            db_obj = DailyTaskState(state=0, statedate=dt, dailytask=dailytask)
            db.add(db_obj)
        await db.commit()

    async def remove_chain(self, db: AsyncSession, user: int, *, fromdate: date, dailytask: int) -> int:
        """
        Called after disabling dailytask.
        Remove all states for dailytask, where date >= fromdate.
        """
        await crud_dailytask.check_access(db, user, uid=dailytask)
        query = delete(DailyTaskState).where(
            DailyTaskState.dailytask == dailytask,
            DailyTaskState.statedate >= fromdate,
        )
        result = await db.execute(query)
        await db.commit()
        return result.rowcount  # type: ignore


dailytaskstate = CRUDDailyTaskState()
