from typing import Optional
from pydantic import BaseModel


class SMsgOut(BaseModel):
    "Service text response"
    msg: str


class SBoolOut(BaseModel):
    "Service bool response"
    state: bool
    msg: Optional[str]
