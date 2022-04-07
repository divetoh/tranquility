from typing import Optional

from pydantic import BaseModel


class SJSONDocOut(BaseModel):
    """ JSONDoc Response """
    uid: int
    doctype: str
    name: str
    jsondoc: str

    class Config:
        orm_mode = True


class SJSONDocUpdate(BaseModel):
    """ JSONDoc Request for update """
    doctype: Optional[str]
    name: Optional[str]
    jsondoc: Optional[str]


class SJSONDocCreate(BaseModel):
    """ JSONDoc Request for create """
    doctype: str = ""
    name: str = ""
    jsondoc: str = ""
