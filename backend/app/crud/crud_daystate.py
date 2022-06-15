from datetime import date
from typing import Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.daystate import DayState
from app.schemas.daystate import SDayStateCreate, SDayStateUpdate


class CRUDDayState():
    async def get(self, db: AsyncSession, user: int, *, statedate: date) -> Optional[DayState]:
        result = await db.execute(select(DayState).filter(
            DayState.user == user,
            DayState.statedate == statedate,
        ))
        res = result.scalars().first()
        return res

    async def get_multi_bydate(self, db: AsyncSession, user: int, *, start: date, end: date) -> list[DayState]:
        """ Get daystates from DB for date range. """
        result = await db.execute(select(DayState).filter(
            DayState.user == user,
            DayState.statedate >= start,
            DayState.statedate <= end,
        ))
        return result.scalars().all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: SDayStateCreate) -> DayState:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = DayState(**obj_in_data, user=user)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: DayState,
        obj_in: Union[SDayStateUpdate, dict[str, Any]],
    ) -> DayState:
        if db_obj.update_bydict(obj_in) > 0:
            await db.commit()
            await db.refresh(db_obj)
        return db_obj


daystate = CRUDDayState()
