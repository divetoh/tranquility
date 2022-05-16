from typing import Any

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, MixinUID, MixinUser


class MemorizeStack(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    section: str = Column(String(100), nullable=False)
    is_active: bool = Column(Boolean(), default=True, nullable=False)
    name: str = Column(String(250), nullable=False)
    description: str = Column(String(1024), nullable=False)

    card_r: Any = relationship(
        "MemorizeCard",
        back_populates="stack_r",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )


class MemorizeCategory(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    name: str = Column(String(100), nullable=False)
    description: str = Column(String(1024), nullable=False)
    color: int = Column(Integer, nullable=False)

    card_r: Any = relationship("MemorizeCard", back_populates="category_r")


class MemorizeCard(Base, MixinUID):
    uid: int = Column(Integer, primary_key=True, index=True)
    stack: int = Column(Integer, ForeignKey("memorizestack.uid", ondelete="CASCADE"), nullable=False, index=True)
    category: int = Column(Integer, ForeignKey("memorizecategory.uid"), nullable=True, index=True)
    is_active: bool = Column(Boolean(), default=True, nullable=False)
    name: str = Column(String(100), nullable=False)
    obverse: str = Column(String(1024), nullable=False)
    reverse: str = Column(String(4096), nullable=False)
    hint: str = Column(String(1024), nullable=True)

    category_r: Any = relationship("MemorizeCategory", back_populates="card_r")
    stack_r: Any = relationship(
        "MemorizeStack",
        back_populates="card_r",
        passive_deletes=True,
    )
