from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base, MixinFolder


class Markdown(Base, MixinFolder):
    uid: int = Column(Integer, primary_key=True, index=True)
    folder: int = Column(Integer, ForeignKey("folder.uid", ondelete="CASCADE"), nullable=False, index=True)
    name: str = Column(String(80), nullable=False)
    md: str = Column(String, nullable=False)

    folder_r: Any = relationship("Folder")
