from typing import Optional

from pydantic import BaseModel


class SToken(BaseModel):
    access_token: str
    token_type: str


class STokenPayload(BaseModel):
    sub: Optional[int] = None
