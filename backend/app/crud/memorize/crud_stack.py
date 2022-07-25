from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud.base import CRUDBaseAuth
from app.models import MemorizeCard, MemorizeCardState, MemorizeStack


class CRUDMemorizeStack(CRUDBaseAuth[MemorizeStack, schemas.SMemorizeStackCreate, schemas.SMemorizeStackUpdate]):
    async def get_stat(self, db: AsyncSession, user: int) -> list:
        corr_answ = {}
        out = []

        # Counting cards by the number of continuous correct answers. Grouped by stacks.
        q = select(func.count(MemorizeCardState.state), MemorizeCardState.state, MemorizeCard.stack).\
            join(MemorizeCard).\
            filter(MemorizeCardState.user == user).\
            group_by(MemorizeCard.stack, MemorizeCardState.state)
        result = await db.execute(q)
        for i in result.all():
            if i[2] not in corr_answ:
                corr_answ[i[2]] = [0] * 10
            if i[1] > 8:
                corr_answ[i[2]][9] += i[0]
            else:
                corr_answ[i[2]][i[1]] = i[0]

        # Get stack info and card count.
        q = select(MemorizeStack.uid, MemorizeStack.name, MemorizeStack.section, func.count(MemorizeCard.uid)).\
            join(MemorizeCard).\
            filter(MemorizeStack.uid.in_(corr_answ.keys())).\
            group_by(MemorizeStack.uid).\
            order_by(MemorizeStack.section, MemorizeStack.name)
        result = await db.execute(q)
        for i in result.all():
            out.append({
                "uid": i[1],
                "name": i[1],
                "section": i[2],
                "count": i[3],
                "unanswered": i[3] - sum(corr_answ[i[0]]),
                "correct": corr_answ[i[0]],
            })

        await db.commit()
        return out


memorizestack = CRUDMemorizeStack(MemorizeStack)
