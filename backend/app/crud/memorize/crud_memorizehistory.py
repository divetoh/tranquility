from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MemorizeCardHistory


class CRUDMemorizeCardHistory():
    async def create(self, db: AsyncSession, user: int, *, card: int, state: int) -> MemorizeCardHistory:
        db_obj = MemorizeCardHistory(user=user, card=card, state=state)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


memorizecardhistory = CRUDMemorizeCardHistory()
