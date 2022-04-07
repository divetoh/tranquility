from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from app.db.base_class import Base, MixinUser


class JSONDoc(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid"), nullable=False, index=True)
    doctype: str = Column(String(20), nullable=False)
    name: str = Column(String(80), nullable=False)
    jsondoc: str = Column(MEDIUMTEXT, nullable=False)
