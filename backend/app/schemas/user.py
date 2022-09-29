from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SUserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str = Field(max_length=80)
    is_active: bool = True
    is_superuser: bool = False


class SUserUpdate(BaseModel):
    full_name: Optional[str] = Field(max_length=2048)
    password: Optional[str] = None
    coreactivity: Optional[int] = None
    coretasklist: Optional[int] = None


class SUserAdminUpdate(SUserUpdate):
    email: Optional[EmailStr]
    is_active: bool = True
    is_superuser: bool = False


class SUser(BaseModel):
    uid: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    full_name: str
    created_dt: datetime
    coreactivity: Optional[int]
    coretasklist: Optional[int]

    class Config:
        orm_mode = True
