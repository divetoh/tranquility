from typing import Optional

from pydantic import BaseModel, Field


class SFolderOut(BaseModel):
    """ Folder Response """
    uid: int
    parent: Optional[int]
    name: str
    foldertype: int

    class Config:
        orm_mode = True


class SFolderUpdate(BaseModel):
    """ Folder Request for update """
    parent: Optional[int]
    name: Optional[str]  = Field(max_length=255)


class SFolderCreate(BaseModel):
    """ Folder Request for create """
    parent: Optional[int]
    name: str = Field(max_length=255)
    foldertype: int


class SFolderContent(BaseModel):
    """ Folder Content Response """
    uid: int
    name: str
    source: str
    type: str

    class Config:
        orm_mode = True
