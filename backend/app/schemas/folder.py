from typing import Optional

from pydantic import BaseModel


class SFolderOut(BaseModel):
    """ Folder Response """
    uid: int
    parent: Optional[str]
    name: str
    foldertype: int

    class Config:
        orm_mode = True


class SFolderUpdate(BaseModel):
    """ Folder Request for update """
    parent: Optional[str]
    name: str


class SFolderCreate(BaseModel):
    """ Folder Request for create """
    parent: Optional[str]
    name: str
    foldertype: int


class SFolderContent(BaseModel):
    """ Folder Content Response """
    uid: int
    name: str
    source: str
    type: str

    class Config:
        orm_mode = True
