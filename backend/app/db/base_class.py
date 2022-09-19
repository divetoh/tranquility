from abc import abstractmethod
from typing import Any, Union

from pydantic import BaseModel
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # Removes mypy error when create model instance
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    # Generate __tablename__ automatically by class name
    @declared_attr
    def __tablename__(cls) -> str:      # noqa
        return cls.__name__.lower()

    def as_dict(self, exclude=None) -> dict:
        """Dict representation of object data"""
        exclude = [] if exclude is None else exclude
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}  # type:ignore

    def update_bydict(self, update_data: Union[BaseModel, dict[str, Any]]) -> int:
        """Updates object by data from dict or Pydantic Model, return number of updated fields"""

        if isinstance(update_data, dict):
            update = update_data
        else:
            update = update_data.dict(exclude_unset=True)

        count = 0
        for col in self.__table__.columns:  # type:ignore
            if col.name in update:
                count += 1
                setattr(self, col.name, update[col.name])
        return count


# Mixins used in Generic CRUD classes

class MixinUID():
    uid: int

    @abstractmethod
    def update_bydict(self, update_data: Union[BaseModel, dict[str, Any]]) -> int:
        pass


class MixinUser(MixinUID):
    user: int


class MixinFolder(MixinUID):
    folder: int
    folder_r: Any
