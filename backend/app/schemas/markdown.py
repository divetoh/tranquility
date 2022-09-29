from typing import Optional
from pydantic import BaseModel, Field


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
    name: Optional[str] = Field(max_length=80)
    md: Optional[str]
    folder: Optional[int]


class SMarkdownCreate(BaseModel):
    """ Markdown Request for create """
    name: str = Field(default="", max_length=80)
    md: str = ""
    folder: int
