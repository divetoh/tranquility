from typing import Optional

from pydantic import BaseModel, Field


class SJSONDocOut(BaseModel):
    """ JSONDoc Response """
    uid: int
    doctype: str
    name: str
    jsondoc: str
    folder: int

    class Config:
        orm_mode = True


class SJSONDocUpdate(BaseModel):
    """ JSONDoc Request for update """
    doctype: Optional[str] = Field(max_length=20)
    name: Optional[str] = Field(max_length=80)
    jsondoc: Optional[str]
    folder: Optional[int]


class SJSONDocCreate(BaseModel):
    """ JSONDoc Request for create """
    doctype: str = Field(default="", max_length=20)
    name: str = Field(default="", max_length=80)
    jsondoc: str = ""
    folder: int
