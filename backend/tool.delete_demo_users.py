"""
If Demo mode is enabled - deletes demo users registred an hour ago.

Demo mode enabled if enviroment variable DEMO_USERS > 0.

Demo users - all users with email like "*@test.test", without administrator rights
"""
import asyncio
from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.db.session import engine


async def go() -> None:
    dbg = get_db()
    db = await dbg.__anext__()
    demo_users = await crud.user.get_demo_users(db)
    for user in demo_users:
        print(f"Delete demo user {user.email}, registered {user.created_dt}")
        await crud.user.remove(db, uid=user.uid)
    await engine.dispose()

if settings.DEMO_USERS == 0:
    print("Demo mode disabled.")
    exit(0)

asyncio.run(go())
