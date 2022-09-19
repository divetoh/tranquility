from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_folder import CRUDBaseFolder
from app.models import JSONDoc, Folder
from app.schemas import SJSONDocCreate, SJSONDocUpdate


class CRUDJSONDoc(CRUDBaseFolder[JSONDoc, SJSONDocCreate, SJSONDocUpdate]):
    async def get_bydoctype(self, db: AsyncSession, user: int, *, doctype: str) -> list[JSONDoc]:
        """ Return users jsondoc filtered by doctype. """
        query = select(JSONDoc).join(Folder).filter(JSONDoc.doctype == doctype, Folder.user == user)
        result = await db.scalars(query)
        return result.all()


jsondoc = CRUDJSONDoc(JSONDoc)
