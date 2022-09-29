from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class SRegularTaskOut(BaseModel):
    """ RegularTask Response """
    uid: int
    is_active: bool
    name: str
    nextdate: date
    period: int

    class Config:
        orm_mode = True


class SRegularTaskUpdate(BaseModel):
    """ RegularTask Request for update """
    is_active: Optional[bool]
    name: Optional[str] = Field(max_length=400)
    nextdate: Optional[date]
    period: Optional[int]


class SRegularTaskCreate(BaseModel):
    """ RegularTask Request for create """
    is_active: bool = True
    name: str = Field(default="", max_length=400)
    nextdate: date
    period: int = 1
