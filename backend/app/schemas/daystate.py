from datetime import date
from typing import Optional
from pydantic import BaseModel


class SDayStateOut(BaseModel):
    """ DayState Response """
    statedate: date
    description: str
    complited: str
    rating: int

    class Config:
        orm_mode = True


class SDayStateUpdate(BaseModel):
    """ DayState Request for update """
    description: Optional[str]
    rating: Optional[int]
    complited: Optional[str]


class SDayStateCreate(BaseModel):
    """ Internal DayState create schema """
    statedate: date
    description: str = ""
    rating: int = 0
    complited: str = "[]"
