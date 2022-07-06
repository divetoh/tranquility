from datetime import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.base_class import Base


class DayState(Base):
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), primary_key=True, index=True)
    statedate: datetime = Column(Date(), primary_key=True, index=True)
    description: str = Column(String(2048))
    rating: int = Column(Integer)
    complited: str = Column(String, default="[]")
