from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBaseAuth
from app.models.jsondoc import JSONDoc
from app.schemas import SJSONDocCreate, SJSONDocUpdate


class CRUDJSONDoc(CRUDBaseAuth[JSONDoc, SJSONDocCreate, SJSONDocUpdate]):
    async def get_bydoctype(self, db: AsyncSession, user: int, *, doctype: str) -> List[JSONDoc]:
        """ Return users jsondoc filtered by doctype. """
        result = await db.execute(select(JSONDoc).filter(JSONDoc.doctype == doctype, JSONDoc.user == user))
        return result.scalars().all()


jsondoc = CRUDJSONDoc(JSONDoc)
