from datetime import date
from typing import Any
from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RegularTaskState(Base):
    statedate: date = Column(Date(), primary_key=True, index=True)
    regulartask: int = Column(Integer, ForeignKey("regulartask.uid", ondelete="CASCADE"), primary_key=True, index=True)
    state: int = Column(Integer, nullable=False, default=0)

    regulartask_r: Any = relationship("RegularTask", back_populates="regulartaskstate_r")
