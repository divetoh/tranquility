from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from app.db.base_class import Base


class DayState(Base):
    user = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), primary_key=True, index=True)
    statedate = Column(Date(), primary_key=True, index=True)
    description = Column(String(2048))
    rating = Column(Integer)
    complited = Column(MEDIUMTEXT, default="[]")
