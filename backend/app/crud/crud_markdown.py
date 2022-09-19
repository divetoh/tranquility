from app.crud.base_folder import CRUDBaseFolder
from app.models.markdown import Markdown
from app.schemas import SMarkdownCreate, SMarkdownUpdate


class CRUDMarkdown(CRUDBaseFolder[Markdown, SMarkdownCreate, SMarkdownUpdate]):
    pass


markdown = CRUDMarkdown(Markdown)
