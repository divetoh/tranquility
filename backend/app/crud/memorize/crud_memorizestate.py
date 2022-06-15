from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MemorizeCardState
from app.schemas import SMemorizeStateCreate


class CRUDMemorizeCardState():
    async def get(self, db: AsyncSession, user: int, *, card: int) -> Optional[MemorizeCardState]:
        """
        Get MemorizeCardState from DB.
        """
        query = select(MemorizeCardState).filter(MemorizeCardState.user == user, MemorizeCardState.card == card)
        result = (await db.execute(query)).scalars().first()
        return result

    async def create(
        self,
        db: AsyncSession,
        user: int,
        *,
        card: int,
        obj_in: SMemorizeStateCreate,
    ) -> MemorizeCardState:
        """
        Create MemorizeCardState
        """
        obj_in_data = obj_in.dict()
        db_obj = MemorizeCardState(**obj_in_data, user=user, card=card)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_byobj(
        self,
        db: AsyncSession,
        user: int,
        *,
        db_obj: MemorizeCardState,
        obj_in: dict[str, Any],
    ) -> MemorizeCardState:
        """
        Update MemorizeCardState from dict. Only filled fields will be updated.
        """
        if db_obj.update_bydict(obj_in) > 0:
            await db.commit()
            await db.refresh(db_obj)
        return db_obj


memorizecardstate = CRUDMemorizeCardState()
