"""
Try connect to database configured in application.

Exit code
* 0:  Database avaliable
* 1: Can't connect to database
"""
import asyncio
import sys
from sqlalchemy import text, MetaData
from app.db.session import engine


MAX_TRIES = 30
WAIT_SECONDS = 5
clear_db = False

async def go() -> int:
    for _ in range(MAX_TRIES):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                if clear_db:
                    print("Database cleanup.")
                    meta = MetaData()
                    await conn.run_sync(meta.reflect)
                    await conn.run_sync(meta.drop_all)
            await engine.dispose()
            # Database avaliable
            return 0
        except Exception:
            pass
        await asyncio.sleep(WAIT_SECONDS)
    await engine.dispose()
    # Error. Database not avaliable
    return 1

if sys.argv[1] == "cleanup":
    clear_db = True

result = asyncio.run(go())
exit(result)
