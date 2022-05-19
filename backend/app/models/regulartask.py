from datetime import date
from typing import Any

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base, MixinUser


class RegularTask(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    is_active: bool = Column(Boolean(), nullable=False, default=True)
    name: str = Column(String(400), nullable=False, default="")
    nextdate: date = Column(Date(), server_default=func.now())
    period: int = Column(Integer, nullable=False, default=1)

    regulartaskstate_r: Any = relationship(
        "RegularTaskState",
        back_populates="regulartask_r",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )
