from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


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
    description: Optional[str] = Field(max_length=2048)
    rating: Optional[int]
    complited: Optional[str]


class SDayStateCreate(BaseModel):
    """ Internal DayState create schema """
    statedate: date
    description: str = Field(default="", max_length=2048)
    rating: int = 0
    complited: str = "[]"
