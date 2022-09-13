from typing import Optional
from pydantic import BaseModel


class SMarkdownOut(BaseModel):
    """ Markdown Response """
    uid: int
    name: str
    md: str
    folder: int

    class Config:
        orm_mode = True


class SMarkdownUpdate(BaseModel):
    """ Markdown Request for update """
    name: Optional[str]
    md: Optional[str]
    folder: Optional[int]


class SMarkdownCreate(BaseModel):
    """ Markdown Request for create """
    name: str = ""
    md: str = ""
    folder: int
