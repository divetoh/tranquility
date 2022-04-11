"""
If user list empty, add initial superuser (from env).
"""
import asyncio
from app import crud, schemas
from app.api.deps import get_db
from app.core.config import settings


async def go() -> None:
    dbg = get_db()
    db = await dbg.__anext__()
    users_count = await crud.user.get_count(db)
    if users_count == 0:
        print("* Creating administrative user.")
        user_in = schemas.SUserCreate(
            full_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(db, obj_in=user_in)

asyncio.run(go())
