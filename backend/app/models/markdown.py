from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from app.db.base_class import Base, MixinUser


class Markdown(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid"), nullable=False, index=True)
    name: str = Column(String(80), nullable=False)
    md: str = Column(MEDIUMTEXT, nullable=False)
