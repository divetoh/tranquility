from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base, MixinUID


class User(Base, MixinUID):
    uid: int = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    full_name: str = Column(String(80), nullable=False)
    email: str = Column(String(80), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(80), nullable=False)
    is_active: bool = Column(Boolean(), default=True, nullable=False)
    is_superuser: bool = Column(Boolean(), default=False, nullable=False)
    coreactivity: Optional[int] = Column(Integer, nullable=True)
    coretasklist: Optional[int] = Column(Integer, nullable=True)
