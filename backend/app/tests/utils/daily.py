from itertools import cycle
from random import randint

from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.tests.utils.utils import random_string


async def cr_rand_dailytask(
    db: AsyncSession,
    uid: int,
    *,
    is_active: bool = True,
) -> dict:
    dailytask = models.DailyTask(user=uid, is_active=is_active, name=random_string())
    db.add(dailytask)
    await db.flush()
    await db.refresh(dailytask)
    await db.commit()
    return dailytask.as_dict()


async def cr_rand_dailytasks(
    db: AsyncSession,
    uid: int,
    count: int,
    *,
    is_active: tuple = (True,),
) -> list[dict]:
    result = []
    for _, is_active_ in zip(range(count), cycle(is_active)):
        dailytask = models.DailyTask(user=uid, is_active=is_active_, name=random_string())
        db.add(dailytask)
        await db.flush()
        await db.refresh(dailytask)
        result.append(dailytask.as_dict())
    await db.commit()
    result.sort(key=lambda x: x["uid"])
    return result


async def cr_rand_dailytaskstates(
    db: AsyncSession,
    dailytask: tuple,
    statedate: tuple,
) -> list[dict]:
    result = []
    for dailytask_ in dailytask:
        for statedate_ in statedate:
            dts = models.DailyTaskState(dailytask=dailytask_, statedate=statedate_, state=randint(0, 2))
            db.add(dts)
            await db.flush()
            await db.refresh(dts)
            result.append(dts.as_dict())
    await db.commit()
    return result
