import uuid
from typing import Optional, Type, Union
from pydantic import BaseModel

from app.core.config import settings
from app.db.base_class import Base

BURL = "http://test" + settings.API_STR


def random_string() -> str:
    return uuid.uuid4().hex


def compare(
    schema: Type[BaseModel],
    one: Union[Base, dict, BaseModel],
    two: Union[Base, dict, BaseModel],
    exclude: Optional[list[str]] = None,
):
    if exclude is None:
        exclude = []
    if isinstance(one, dict):
        one = schema(**one)
    if isinstance(two, dict):
        two = schema(**two)
    for fld in schema.__fields__:
        if fld in exclude:
            continue
        assert getattr(one, fld) == getattr(two, fld)
