# Import data from JSON file for new user

import json
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas


async def import_regulartask(db: AsyncSession, user: int, data: dict) -> dict[int, int]:
    # Import regular tasks and states
    map_regulartask: dict[int, models.RegularTask] = {}

    for i in data.get('regulartask', []):
        sc_rt = schemas.SRegularTaskCreate(**i)
        db_obj = models.RegularTask(user=user, **sc_rt.dict())
        map_regulartask[i["uid"]] = db_obj
    db.add_all(map_regulartask.values())
    await db.flush()

    for i in data.get('regulartaskstate', []):
        sc_rts = schemas.SRegularTaskStateCreate(**i)
        sc_rts.regulartask = map_regulartask[i["regulartask"]].uid
        db.add(models.RegularTaskState(**sc_rts.dict()))

    await db.flush()
    return {juid: map_regulartask[juid].uid for juid in map_regulartask}


async def import_dailytask(db: AsyncSession, user: int, data: dict) -> dict[int, int]:
    # Import daily tasks and states
    map_dailytask: dict[int, models.DailyTask] = {}

    for i in data.get('dailytask', []):
        sc_dt = schemas.SDailyTaskCreate(**i)
        db_obj = models.DailyTask(user=user, **sc_dt.dict())
        map_dailytask[i["uid"]] = db_obj
    db.add_all(map_dailytask.values())
    await db.flush()

    for i in data.get('dailytaskstate', []):
        sc_dts = schemas.SDailyTaskStateCreate(**i)
        sc_dts.dailytask = map_dailytask[i["dailytask"]].uid
        db.add(models.DailyTaskState(**sc_dts.dict()))

    await db.flush()
    return {juid: map_dailytask[juid].uid for juid in map_dailytask}


async def import_daystate(db: AsyncSession, user: int, data: dict) -> None:
    # Import day states
    for i in data.get('daystate', []):
        sc_ds = schemas.SDayStateCreate(**i)
        db_obj = models.DayState(user=user, **sc_ds.dict())
        db.add(db_obj)
    await db.flush()


async def import_markdown(db: AsyncSession, user: int, data: dict) -> dict[int, int]:
    # Import markdown
    map_markdown: dict[int, models.Markdown] = {}

    for i in data.get('markdown', []):
        sc_md = schemas.SMarkdownCreate(**i)
        obj_md = models.Markdown(user=user, **sc_md.dict())
        map_markdown[i["uid"]] = obj_md

    db.add_all(map_markdown.values())
    await db.flush()
    return {juid: map_markdown[juid].uid for juid in map_markdown}


async def import_memorize(db: AsyncSession, user: int, data: dict) -> None:
    map_category: dict[int, models.MemorizeCategory] = {}
    map_stack: dict[int, models.MemorizeStack] = {}

    for i in data.get('memorizecategory', []):
        sc_mc = schemas.SMemorizeCategoryCreate(**i)
        mc = models.MemorizeCategory(user=user, **sc_mc.dict())
        map_category[i["uid"]] = mc

    for i in data.get('memorizestack', []):
        sc_ms = schemas.SMemorizeStackCreate(**i)
        ms = models.MemorizeStack(user=user, **sc_ms.dict())
        map_stack[i["uid"]] = ms

    db.add_all(map_category.values())
    db.add_all(map_stack.values())
    await db.flush()

    for i in data.get('memorizecard', []):
        sc_c = schemas.SMemorizeCardCreate(**i)
        sc_c.stack = map_stack[i["stack"]].uid
        if i["category"] is not None:
            sc_c.category = map_category[i["category"]].uid
        db.add(models.MemorizeCard(**sc_c.dict()))

    await db.flush()


def replace_tasklist_uid(jsondoc: str, map_regulartask: dict[int, int], map_dailytask: dict[int, int]) -> str:
    # Replace uid for daily state and dailytask in jsondoc
    try:
        temp_jd = json.loads(jsondoc)
        for j in temp_jd:
            if "type" in j and j["type"] == "regulartask":
                j["regulartask"] = map_regulartask[j["regulartask"]]
            elif "type" in j and j["type"] == "dailytask":
                j["dailytask"] = map_dailytask[j["dailytask"]]
        return json.dumps(temp_jd, default=str, ensure_ascii=False)
    except Exception:
        return jsondoc


def replace_workspace_uid(
    jsondoc: str,
    map_markdown: dict[int, int],
    map_jsondoc: dict[int, models.JSONDoc],
) -> str:
    # Replace uid for markdown and tasklist in workspace jsondoc
    try:
        temp_jd = json.loads(jsondoc)
        for j in temp_jd["content"]:
            for k in j["content"]:
                if k["type"] == "markdown":
                    k["uid"] = map_markdown[k["uid"]]
                elif k["type"] == "tasklist":
                    k["uid"] = map_jsondoc[k["uid"]].uid
        return json.dumps(temp_jd, default=str, ensure_ascii=False)
    except Exception:
        return jsondoc


def replace_activity_uid(
    jsondoc: str,
    map_jsondoc: dict[int, models.JSONDoc],
) -> str:
    # Replace uid for workspaces in activity jsondoc
    try:
        temp_jd = json.loads(jsondoc)
        for j in range(len(temp_jd["workspaces"])):
            temp_jd["workspaces"][j] = map_jsondoc[temp_jd["workspaces"][j]].uid
        return json.dumps(temp_jd, default=str, ensure_ascii=False)
    except Exception:
        return jsondoc


async def import_data(db: AsyncSession, db_obj: models.User, data_source: str) -> models.User:
    # Open file with initial data
    userid = db_obj.uid
    with open("initdata/" + data_source) as f:
        data = json.load(f)

    map_regulartask = await import_regulartask(db, userid, data)
    map_dailytask = await import_dailytask(db, userid, data)
    await import_daystate(db, userid, data)
    map_markdown = await import_markdown(db, userid, data)
    await import_memorize(db, userid, data)
    map_jsondoc: dict[int, models.JSONDoc] = {}

    # Import tasklists
    for i in data['jsondoc']:
        if i["doctype"] != "tasklist":
            continue
        new_jsondoc = replace_tasklist_uid(i["jsondoc"], map_regulartask, map_dailytask)
        sc_jd = schemas.SJSONDocCreate(**(i | {"jsondoc": new_jsondoc}))
        obj_jd = models.JSONDoc(user=userid, **sc_jd.dict())
        db.add(obj_jd)
        map_jsondoc[i["uid"]] = obj_jd
    await db.flush()

    # Import workspaces
    for i in data['jsondoc']:
        if i["doctype"] != "workspace":
            continue
        new_jsondoc = replace_workspace_uid(i["jsondoc"], map_markdown, map_jsondoc)
        sc_jd = schemas.SJSONDocCreate(**(i | {"jsondoc": new_jsondoc}))
        obj_jd = models.JSONDoc(user=userid, **sc_jd.dict())
        db.add(obj_jd)
        map_jsondoc[i["uid"]] = obj_jd
    await db.flush()

    # Import activity
    for i in data['jsondoc']:
        if i["doctype"] != "activity":
            continue
        new_jsondoc = replace_activity_uid(i["jsondoc"], map_jsondoc)
        sc_jd = schemas.SJSONDocCreate(**(i | {"jsondoc": new_jsondoc}))
        obj_jd = models.JSONDoc(user=userid, **sc_jd.dict())
        db.add(obj_jd)
        map_jsondoc[i["uid"]] = obj_jd
    await db.commit()

    obj_upd = {
        "coreactivity": map_jsondoc[data["coreactivity"]].uid,
        "coretasklist": map_jsondoc[data["coretasklist"]].uid,
    }
    return await crud.user.update_byobj(db=db, db_obj=db_obj, obj_in=obj_upd)
