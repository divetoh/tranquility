from sqlalchemy import select, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Union

from app.crud.base_auth import CRUDBaseAuth
from app.models.folder import Folder
from app.models.jsondoc import JSONDoc
from app.models.markdown import Markdown
from app.schemas import SFolderCreate, SFolderContent, SFolderUpdate


class CRUDFolder(CRUDBaseAuth[Folder, SFolderCreate, SFolderUpdate]):
    async def get_content(self, db: AsyncSession, user: int, *, folder: int) -> Any:
        """ Return content of folder. """
        await self.check_access(db, user, uid=folder)
        query1 = select(JSONDoc.uid, JSONDoc.name, literal_column("'jsondoc'").label("source"),
                        JSONDoc.doctype.label("type")).filter(JSONDoc.folder == folder)
        query2 = select(Markdown.uid, Markdown.name, literal_column("'markdown'").label("source"),
                        literal_column("'markdown'").label("type")).filter(Markdown.folder == folder)
        query = query1.union(query2).order_by("name")
        result = await db.execute(query)
        return result.all()

    async def create(self, db: AsyncSession, user: int, *, obj_in: SFolderCreate) -> Folder:
        await self.check_access(db, user, uid=obj_in.parent)
        return await super().create(db, user, obj_in=obj_in)

    # TODO: modify update (check access)


folder = CRUDFolder(Folder)
