from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base, MixinFolder


class JSONDoc(Base, MixinFolder):
    uid: int = Column(Integer, primary_key=True, index=True)
    folder: int = Column(Integer, ForeignKey("folder.uid", ondelete="CASCADE"), nullable=False, index=True)
    doctype: str = Column(String(20), nullable=False)
    name: str = Column(String(80), nullable=False)
    jsondoc: str = Column(JSONB, nullable=False)

    folder_r: Any = relationship("Folder")
