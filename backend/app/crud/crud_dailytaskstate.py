from datetime import date
from typing import Any, Optional, Union

from sqlalchemy import delete, literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DailyTask, DailyTaskState
from app.schemas.dailytaskstate import SDailyTaskStateCreate, SDailyTaskStateUpdate
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

    async def create(self, db: AsyncSession, user: int, *, obj_in: SDailyTaskStateCreate) -> DailyTaskState:
        await crud_dailytask.check_access(db, user, uid=obj_in.dailytask)
        obj_in_data = obj_in.dict()
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
        if db_obj.update_bydict(obj_in) > 0:
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def create_chain(self, db: AsyncSession, user: int, *, fromdate: date, dailytask: int) -> None:
        """
        Called after creation/enabling dailytask.
        Search all days>=`fromdate`, which allready have status for any dailytask,
        and add status for `dailytask` to this day.
        """
        dates = select(DailyTaskState.statedate, literal(dailytask), literal(0)).join(DailyTask).filter(
            DailyTask.user == user,
            DailyTaskState.statedate >= fromdate,
        ).group_by(DailyTaskState.statedate)
        table = DailyTaskState.__table__    # type: ignore
        query = table.insert().from_select(['statedate', 'dailytask', 'state'], dates)
        await db.execute(query)
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
