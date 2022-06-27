from datetime import datetime
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.security import create_access_token, get_password_hash
from app.tests.utils.utils import random_string


async def cr_rand_user(
    db: AsyncSession,
    *,
    email: str = None,
    full_name: str = None,
    password: str = None,
    is_superuser: bool = False,
    is_active: bool = True,
    created_dt: Optional[datetime] = None,
    coreactivity: Optional[int] = None,
    coretasklist: Optional[int] = None,
) -> models.User:
    """  Generate User Accounts with random parameters  """

    user_dict: dict[str, Any] = {
        "email": email or random_string() + "@test.test",
        "full_name": full_name or random_string(),
        "hashed_password": get_password_hash(password or random_string()),
        "is_superuser": is_superuser,
        "is_active": is_active,
        "created_dt": created_dt,
        "coreactivity": coreactivity,
        "coretasklist": coretasklist,
    }
    if created_dt is not None:
        user_dict["created_dt"] = created_dt
    user = models.User(**user_dict)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    await db.commit()
    return user


def user_token(user: models.User) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.uid)}"}
