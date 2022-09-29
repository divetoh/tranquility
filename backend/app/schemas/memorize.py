from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, conlist, Field


class SMemorizeStackOut(BaseModel):
    """ Memory Card Stack Response """
    uid: int
    section: str
    is_active: bool
    name: str
    description: str

    class Config:
        orm_mode = True


class SMemorizeStackCreate(BaseModel):
    """ Memory Card Stack Request for create """
    section: str = Field(max_length=100)
    is_active: bool = True
    name: str = Field(max_length=250)
    description: str = Field(default="", max_length=1024)


class SMemorizeStackUpdate(BaseModel):
    """ Memory Card Stack Request for update """
    section: Optional[str] = Field(max_length=100)
    is_active: Optional[bool]
    name: Optional[str] = Field(max_length=250)
    description: Optional[str] = Field(max_length=1024)


class SMemorizeCardsReadyCount(BaseModel):
    """ Memory Card counted by answered/ready """
    cards: int
    untimely: int
    ready: int


class SMemorizeCategoryOut(BaseModel):
    """ Memory Card Category Response """
    uid: int
    name: str
    description: str
    color: int

    class Config:
        orm_mode = True


class SMemorizeCategoryCreate(BaseModel):
    """ Memory Card Category Request for create """
    name: str = Field(max_length=100)
    description: str = Field(default="", max_length=1024)
    color: int = 0


class SMemorizeCategoryUpdate(BaseModel):
    """ Memory Card Category Request for update """
    name: Optional[str] = Field(max_length=100)
    description: Optional[str] = Field(max_length=1024)
    color: Optional[int]


class SMemorizeCardStateOut(BaseModel):
    state: int
    lastdate: date
    nextdate: date

    class Config:
        orm_mode = True


class SMemorizeCardBaseOut(BaseModel):
    """ Memory Card Response """
    uid: int
    stack: int
    category: Optional[int]
    is_active: bool
    name: str
    obverse: str
    reverse: str
    hint: Optional[str]

    class Config:
        orm_mode = True


class SMemorizeCardOut(SMemorizeCardBaseOut):
    """ Memory Card Response with state"""
    state_r: conlist(SMemorizeCardStateOut, min_items=0, max_items=1)  # type: ignore

    class Config:
        orm_mode = True


class SMemorizeCardCreate(BaseModel):
    """ Memory Card Request for create """
    stack: int
    category: Optional[int]
    is_active: bool = True
    name: str = Field(max_length=100)
    obverse: str = Field(max_length=1024)
    reverse: str = Field(max_length=4096)
    hint: Optional[str] = Field(max_length=1024)


class SMemorizeCardUpdate(BaseModel):
    """ Memory Card Request for update """
    stack: Optional[int]
    category: Optional[int]
    is_active: Optional[bool]
    name: Optional[str] = Field(max_length=100)
    obverse: Optional[str] = Field(max_length=1024)
    reverse: Optional[str] = Field(max_length=4096)
    hint: Optional[str] = Field(max_length=1024)


class SMemorizeCardOutHistory(BaseModel):
    """ Memory Card History Response """
    history: list[tuple[datetime, int]]
    attempts: int
    correct: int


class SMemorizeAnswerIn(BaseModel):
    """ MemorizeCard answered """
    state: int
    answerdate: date


class SMemorizeStateCreate(BaseModel):
    """ MemorizeCardState create """
    state: int
    lastdate: date
    nextdate: Optional[date]


class SMemorizeHistoryOut(BaseModel):
    """ MemorizeCardHistory response """
    uid: int
    card: int
    state: int
    statedate: datetime

    class Config:
        orm_mode = True


class SMemorizeStateOut(BaseModel):
    """ MemorizeCardState response """
    card: int
    state: int
    lastdate: date
    nextdate: Optional[date]

    class Config:
        orm_mode = True


class SMemorizeAnswerOut(BaseModel):
    state: SMemorizeStateOut
    history: SMemorizeHistoryOut
