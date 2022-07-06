"""
Migrate data from mariadb to postgresql.
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app import models
from app.core.config import settings

MAX_TRIES = 30
WAIT_SECONDS = 5
old_dbe = create_async_engine(settings.SQLALCHEMY_OLDDATABASE_URI, pool_pre_ping=True, pool_recycle=3600)
new_dbe = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_recycle=3600)


async def get_connection(engine):
    for _ in range(MAX_TRIES):
        try:
            conn = await engine.connect()
            await conn.execute(text("SELECT 1"))
            return conn
        except Exception:
            pass
        await asyncio.sleep(WAIT_SECONDS)
    return None


async def migrate_user(mdb, pg):
    """ All Users records must be migrated """
    print(">>> Migrating User start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, full_name, email, hashed_password, is_active, is_superuser, coreactivity,"
                                 " coretasklist, created_dt FROM user"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(
                ("uid", "full_name", "email", "hashed_password", "is_active", "is_superuser", "coreactivity",
                 "coretasklist", "created_dt"),
                i,
            ))
            await pg.execute(models.User.__table__.insert().values(val))
        except Exception:
            await pg.rollback()
            print("   Error: can't migrate user record: ", val)
            await mdb.close()
            await pg.close()
            await old_dbe.dispose()
            await new_dbe.dispose()
            exit(4)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('user', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating User complite\n")


async def migrate_daystate(mdb, pg):
    """ Ignore errors """
    print(">>> Migrating DayState start")
    sel = await mdb.execute(text("SELECT user, statedate, description, rating, complited FROM daystate"))
    for i in sel.all():
        try:
            val = dict(zip(("user", "statedate", "description", "rating", "complited"), i))
            await pg.execute(models.DayState.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate daystate record, ignored: ", val)
    print("+++ Migrating DayState comlite\n")


async def migrate_dailytask(mdb, pg):
    """ Ignore errors, skip states for ignored tasks """
    print(">>> Migrating DailyTask start")
    max_uid = 0
    ignored_dt = []
    sel = await mdb.execute(text("SELECT uid, user, is_active, name FROM dailytask"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "is_active", "name"), i))
            await pg.execute(models.DailyTask.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            ignored_dt.append(i[0])
            await pg.rollback()
            print("   Can't migrate dailytask record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('dailytask', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating DailyTask comlite\n")
    print(">>> Migrating DailyTaskState start")
    sel = await mdb.execute(text("SELECT statedate, dailytask, state FROM dailytaskstate"))
    for i in sel.all():
        if i[1] in ignored_dt:
            continue
        try:
            val = dict(zip(("statedate", "dailytask", "state"), i))
            await pg.execute(models.DailyTaskState.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate dailytaskstate record, ignored: ", val)
    print("+++ Migrating DailyTaskState comlite\n")


async def migrate_regulartask(mdb, pg):
    """ Ignore errors, skip states for ignored tasks """
    print(">>> Migrating RegularTask start")
    max_uid = 0
    ignored_rt = []
    sel = await mdb.execute(text("SELECT uid, user, is_active, name, nextdate, period FROM regulartask"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "is_active", "name", "nextdate", "period"), i))
            await pg.execute(models.RegularTask.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            ignored_rt.append(i[0])
            await pg.rollback()
            print("   Can't migrate dailytask record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('regulartask', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating RegularTask comlite\n")
    print(">>> Migrating RegularTaskState start")
    sel = await mdb.execute(text("SELECT statedate, regulartask, state FROM regulartaskstate"))
    for i in sel.all():
        if i[1] in ignored_rt:
            continue
        try:
            val = dict(zip(("statedate", "regulartask", "state"), i))
            await pg.execute(models.RegularTaskState.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate dailytaskstate record, ignored: ", val)
    print("+++ Migrating RegularTaskState comlite\n")


async def migrate_markdown(mdb, pg):
    """ Ignore errors """
    print(">>> Migrating Markdown start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, user, name, md FROM markdown"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "name", "md"), i))
            await pg.execute(models.Markdown.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate markdown record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('markdown', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating Markdown comlite\n")


async def migrate_jsondoc(mdb, pg):
    """ Ignore errors """
    print(">>> Migrating JSONDoc start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, user, doctype, name, jsondoc FROM jsondoc"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "doctype", "name", "jsondoc"), i))
            await pg.execute(models.JSONDoc.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate jsondoc record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('jsondoc', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating JSONDoc comlite\n")


async def migrate_memorize(mdb, pg):
    """ Ignore errors """
    print(">>> Migrating MemorizeCategory start")
    ignored_mc, ignored_ms, ignored_c = [], [], []
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, user, name, description, color FROM memorizecategory"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "name", "description", "color"), i))
            await pg.execute(models.MemorizeCategory.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            ignored_mc.append(i[0])
            await pg.rollback()
            print("   Can't migrate memorizecategory record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('memorizecategory', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating MemorizeCategory comlite\n")

    print(">>> Migrating MemorizeStack start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, user, section, is_active, name, description FROM memorizestack"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            val = dict(zip(("uid", "user", "section", "is_active", "name", "description", "color"), i))
            await pg.execute(models.MemorizeStack.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            ignored_ms.append(i[0])
            await pg.rollback()
            print("   Can't migrate memorizestack record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('memorizestack', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating MemorizeStack comlite\n")

    print(">>> Migrating MemorizeCard start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, stack, category, is_active, name, obverse, reverse, hint "
                                 "FROM memorizecard"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            if i[1] in ignored_ms:
                ignored_c.append(i[0])
                continue
            val = dict(zip(("uid", "stack", "category", "is_active", "name", "obverse", "reverse", "hint"), i))
            if val["category"] in ignored_mc:
                val["category"] = None
            await pg.execute(models.MemorizeCard.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            ignored_c.append(i[0])
            await pg.rollback()
            print("   Can't migrate memorizecard record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('memorizecard', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating MemorizeCard comlite\n")

    print(">>> Migrating MemorizeCardState start")
    sel = await mdb.execute(text("SELECT user, card, state, lastdate, nextdate FROM memorizecardstate"))
    for i in sel.all():
        try:
            if i[1] in ignored_c:
                continue
            val = dict(zip(("user", "card", "state", "lastdate", "nextdate"), i))
            await pg.execute(models.MemorizeCardState.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate memorizecardstate record, ignored: ", val)
    print("+++ Migrating MemorizeCardState comlite\n")

    print(">>> Migrating MemorizeCardHistory start")
    max_uid = 0
    sel = await mdb.execute(text("SELECT uid, user, card, state, statedate FROM memorizecardhistory"))
    for i in sel.all():
        try:
            max_uid = max(max_uid, int(i[0]))
            if i[2] in ignored_c:
                continue
            val = dict(zip(("uid", "user", "card", "state", "statedate"), i))
            await pg.execute(models.MemorizeCardHistory.__table__.insert().values(val))
            await pg.commit()
        except Exception:
            await pg.rollback()
            print("   Can't migrate memorizecardhistory record, ignored: ", val)
    await pg.execute(text(f"SELECT setval(pg_get_serial_sequence('memorizecardhistory', 'uid'), {max_uid+1});"))
    await pg.commit()
    print("+++ Migrating MemorizeCardHistory comlite\n")


async def go() -> int:
    mdb = await get_connection(old_dbe)
    if mdb is None:
        print("Error: can't connect to MariaDB server")
        exit(1)
    pg = await get_connection(new_dbe)
    if pg is None:
        print("Error: can't connect to PostgreSQL server")
        await mdb.close()
        await old_dbe.dispose()
        exit(2)

    try:
        res = await mdb.execute(text("select * from alembic_version"))
        await mdb.commit()
        ver = res.first()[0]
        assert ver == "cb28b4bb59e6"
    except Exception:
        print("Error: MariaDB schema version must be updated to 0.1.5 (cb28b4bb59e6) before migration.")
        await mdb.close()
        await pg.close()
        await old_dbe.dispose()
        await new_dbe.dispose()
        exit(3)

    try:
        res = await pg.execute(text("select * from alembic_version"))
        await pg.commit()
        ver = res.first()[0]
        assert ver == "a9dc3ed4b0e7"
    except Exception:
        print("Error: PostreSQL schema version must be updated to 0.2.01 (a9dc3ed4b0e7) before migration.")
        await mdb.close()
        await pg.close()
        await old_dbe.dispose()
        await new_dbe.dispose()
        exit(3)

    await migrate_user(mdb, pg)
    await migrate_daystate(mdb, pg)
    await migrate_dailytask(mdb, pg)
    await migrate_regulartask(mdb, pg)
    await migrate_markdown(mdb, pg)
    await migrate_jsondoc(mdb, pg)
    await migrate_memorize(mdb, pg)

    await mdb.close()
    await pg.close()
    await old_dbe.dispose()
    await new_dbe.dispose()
    return 0

result = asyncio.run(go())
exit(result)
