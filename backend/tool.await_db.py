"""
Try connect to database configured in application.

Exit code
* 0:  Database avaliable
* 1: Can't connect to database
"""
import asyncio
from sqlalchemy import text
from app.db.session import engine


MAX_TRIES = 10
WAIT_SECONDS = 3


async def go() -> int:
    for _ in range(MAX_TRIES):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            # Database avaliable
            return 0
        except Exception:
            pass
        await asyncio.sleep(WAIT_SECONDS)
    await engine.dispose()
    # Error. Database not avaliable
    return 1

result = asyncio.run(go())
exit(result)
