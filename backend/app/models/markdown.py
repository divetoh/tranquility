from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base, MixinUser


class Markdown(Base, MixinUser):
    uid: int = Column(Integer, primary_key=True, index=True)
    user: int = Column(Integer, ForeignKey("user.uid", ondelete="CASCADE"), nullable=False, index=True)
    name: str = Column(String(80), nullable=False)
    md: str = Column(String, nullable=False)
