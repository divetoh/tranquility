from datetime import date
from typing import Any
from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DailyTaskState(Base):
    statedate: date = Column(Date(), primary_key=True, index=True)
    dailytask: int = Column(Integer, ForeignKey("dailytask.uid", ondelete="CASCADE"), primary_key=True, index=True)
    state: int = Column(Integer, nullable=False, default=0)

    dailytask_r: Any = relationship("DailyTask", back_populates="dailytaskstate_r")
