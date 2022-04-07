from datetime import date
from pydantic import BaseModel


class SRegularTaskStateOut(BaseModel):
    """ RegularTaskState Response """
    statedate: date
    regulartask: int
    state: int

    class Config:
        orm_mode = True


class SRegularTaskStateCreate(BaseModel):
    """ RegularTaskState Request for create """
    statedate: date
    regulartask: int
    state: int = 0
