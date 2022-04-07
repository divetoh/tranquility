from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False


class SUserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    coreactivity: Optional[int] = None
    coretasklist: Optional[int] = None


class SUserAdminUpdate(SUserUpdate):
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_superuser: bool = False


class SUser(BaseModel):
    uid: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    full_name: str
    coreactivity: Optional[int]
    coretasklist: Optional[int]

    class Config:
        orm_mode = True
