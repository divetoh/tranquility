from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MemorizeCardHistory
from app.schemas import SMemorizeCardOutHistory


class CRUDMemorizeCardHistory():
    async def create(self, db: AsyncSession, user: int, *, card: int, state: int) -> MemorizeCardHistory:
        db_obj = MemorizeCardHistory(user=user, card=card, state=state)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_histroy(self, db: AsyncSession, user: int, *, card: int) -> SMemorizeCardOutHistory:
        q = select(MemorizeCardHistory.statedate, MemorizeCardHistory.state).\
            filter(MemorizeCardHistory.user == user, MemorizeCardHistory.card == card).\
            order_by(MemorizeCardHistory.statedate.desc())
        result = await db.execute(q)
        history = []
        correct = 0
        for lst in result.all():
            history.append(tuple(lst))
            correct += lst[1]
        out = SMemorizeCardOutHistory(history=history, attempts=len(history), correct=correct)
        return out


memorizecardhistory = CRUDMemorizeCardHistory()
