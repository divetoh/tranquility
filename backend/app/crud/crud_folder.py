from sqlalchemy import select, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.crud.base import CRUDBaseAuth
from app.models.folder import Folder
from app.models.jsondoc import JSONDoc
from app.models.markdown import Markdown
from app.schemas import SFolderCreate, SFolderContent, SFolderUpdate


class CRUDFolder(CRUDBaseAuth[Folder, SFolderCreate, SFolderUpdate]):
    async def get_content(self, db: AsyncSession, user: int, *, folder: int) -> Any:
        """ Return content of folder. """
        # Check folder own rights
        query1 = select(JSONDoc.uid, JSONDoc.name, literal_column("'jsondoc'").label("source"),
                        JSONDoc.doctype.label("type")).filter(JSONDoc.folder == folder, JSONDoc.user == user)
        query2 = select(Markdown.uid, Markdown.name, literal_column("'markdown'").label("source"),
                        literal_column("'markdown'").label("type")).filter(Markdown.folder == folder, Markdown.user == user)
        query = query1.union(query2).order_by("name")
        result = await db.execute(query)
        return result.all()

folder = CRUDFolder(Folder)
