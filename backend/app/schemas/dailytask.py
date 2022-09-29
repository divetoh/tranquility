from typing import Optional
from pydantic import BaseModel, Field


class SDailyTaskOut(BaseModel):
    """ DailyTask Response """
    uid: int
    is_active: bool
    name: str

    class Config:
        orm_mode = True


class SDailyTaskUpdate(BaseModel):
    """ DailyTask Request for update """
    is_active: Optional[bool]
    name: Optional[str] = Field(max_length=400)


class SDailyTaskCreate(BaseModel):
    """ DailyTask Request for create """
    is_active: bool = True
    name: str = Field(max_length=400)
