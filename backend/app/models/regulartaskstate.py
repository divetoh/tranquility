from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer

from app.db.base_class import Base


class RegularTaskState(Base):
    statedate: date = Column(Date(), primary_key=True, index=True)
    regulartask: int = Column(Integer, ForeignKey("regulartask.uid", ondelete="CASCADE"), primary_key=True, index=True)
    state: int = Column(Integer, nullable=False, default=0)

    # regulartask_r - back_ref relationship
