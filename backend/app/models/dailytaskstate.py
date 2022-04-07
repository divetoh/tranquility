from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer

from app.db.base_class import Base


class DailyTaskState(Base):
    statedate: date = Column(Date(), primary_key=True, index=True)
    dailytask: int = Column(Integer, ForeignKey("dailytask.uid", ondelete="CASCADE"), primary_key=True, index=True)
    state: int = Column(Integer, nullable=False, default=0)

    # dailytask_r - back_ref relationship
