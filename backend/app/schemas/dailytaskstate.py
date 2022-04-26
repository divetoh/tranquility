from datetime import date
from pydantic import BaseModel


class SDailyTaskStateOut(BaseModel):
    """ DailyTaskState Response """
    statedate: date
    dailytask: int
    state: int

    class Config:
        orm_mode = True


class SDailyTaskStateUpdate(BaseModel):
    """ DailyTaskState Request for update """
    state: int = 0


class SDailyTaskStateCreate(BaseModel):
    """ DailyTaskState Create """
    statedate: date
    dailytask: int
    state: int
