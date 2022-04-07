from app.crud.base import CRUDBaseAuth
from app.models.markdown import Markdown
from app.schemas import SMarkdownCreate, SMarkdownUpdate


class CRUDMarkdown(CRUDBaseAuth[Markdown, SMarkdownCreate, SMarkdownUpdate]):
    pass


markdown = CRUDMarkdown(Markdown)
