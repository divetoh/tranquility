from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base, MixinUser


class Folder(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    parent: int = Column(Integer, ForeignKey("folder.uid", ondelete="CASCADE"), nullable=True, index=True)
    name: str = Column(String(255), nullable=False)
    foldertype: int = Column(Integer, nullable=False, default=1)

