from datetime import date
from typing import Any, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.daystate import DayState
from app.schemas.daystate import SDayStateCreate, SDayStateUpdate


class CRUDDayState():
    async def get(self, db: AsyncSession, user: int, *, statedate: date) -> Optional[DayState]:
        result = await db.scalars(select(DayState).filter(
            DayState.user == user,
            DayState.statedate == statedate,
        ))
        res = result.first()
        await db.commit()
        return res

    async def get_multi_bydate(self, db: AsyncSession, user: int, *, start: date, end: date) -> list[DayState]:
        """ Get daystates from DB for date range. """
        result = await db.scalars(select(DayState).filter(
            DayState.user == user,
            DayState.statedate >= start,
            DayState.statedate <= end,
        ))
        await db.commit()
        return result.all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: SDayStateCreate) -> Optional[DayState]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = DayState(**obj_in_data, user=user)
        try:
            db.add(db_obj)
            await db.flush()
            await db.refresh(db_obj)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            return None
        return db_obj

    async def update_byobj(
        self,
        db: AsyncSession,
        *,
        db_obj: DayState,
        obj_in: Union[SDayStateUpdate, dict[str, Any]],
    ) -> DayState:
        if db_obj.update_bydict(obj_in) > 0:
            await db.flush()
            await db.refresh(db_obj)
            await db.commit()
        return db_obj


daystate = CRUDDayState()
