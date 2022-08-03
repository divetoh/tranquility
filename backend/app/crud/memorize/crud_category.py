from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import true

from app import schemas
from app.crud.base import CRUDBaseAuth
from app.models import MemorizeCard, MemorizeCardState, MemorizeCategory


class CRUDMemorizeCategory(CRUDBaseAuth[
    MemorizeCategory,
    schemas.SMemorizeCategoryCreate,
    schemas.SMemorizeCategoryUpdate,
]):
    async def get_readycount(
        self,
        db: AsyncSession,
        user: int,
        dt: date,
    ) -> dict[int, schemas.SMemorizeCardsReadyCount]:
        out = {}

        # Cards, that don't need check (for dt date).
        answered_q = select(MemorizeCardState.card).where(MemorizeCardState.nextdate > dt).subquery()
        # Count cards by category.
        q = select(MemorizeCard.category, func.count(MemorizeCard.uid), func.count(answered_q.c.card)).\
            outerjoin(answered_q, MemorizeCard.uid == answered_q.c.card).\
            filter(MemorizeCard.is_active == true()).\
            group_by(MemorizeCard.category)
        result = await db.execute(q)

        for i in result.all():
            if i[0] is None:
                continue
            out[i[0]] = schemas.SMemorizeCardsReadyCount(
                cards=i[1],
                untimely=i[2],
                ready=i[1] - i[2],
            )
        return out


memorizecategory = CRUDMemorizeCategory(MemorizeCategory)
