from typing import Any

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, MixinUser


class DailyTask(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    is_active: bool = Column(Boolean(), nullable=False, default=True)
    name: str = Column(String(400), nullable=False)

    dailytaskstate_r: Any = relationship(
        "DailyTaskState",
        back_populates="dailytask_r",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )
