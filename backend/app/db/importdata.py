# Import data from JSON file for new user

import json
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas


async def import_data(db: AsyncSession, db_obj: models.User, data_source: str) -> models.User:
    # Open file with initial data
    userid = db_obj.uid
    with open("initdata/" + data_source) as f:
        data = json.load(f)
    map_regulartask: dict[int, int] = {}
    map_dailytask: dict[int, int] = {}
    map_markdown: dict[int, int] = {}
    map_jsondoc: dict[int, int] = {}

    # Import regular tasks and states
    for i in data['regulartask']:
        uid = i["uid"]
        del i["uid"]
        sc_rt = schemas.SRegularTaskCreate(**i)
        obj_rt = await crud.regulartask.create(db, userid, obj_in=sc_rt)
        map_regulartask[uid] = obj_rt.uid
    for i in data['regulartaskstate']:
        try:
            i["regulartask"] = map_regulartask[i["regulartask"]]
            sc_rts = schemas.SRegularTaskStateCreate(**i)
            await crud.regulartaskstate.create(db, userid, obj_in=sc_rts)
        except Exception:
            print(f"Can't create regulartaskstate: {i}")

    # Import daily tasks and states
    for i in data['dailytask']:
        uid = i["uid"]
        del i["uid"]
        sc_dt = schemas.SDailyTaskCreate(**i)
        obj_dt = await crud.dailytask.create(db, userid, obj_in=sc_dt)
        map_dailytask[uid] = obj_dt.uid
    for i in data['dailytaskstate']:
        try:
            i["dailytask"] = map_dailytask[i["dailytask"]]
            sc_dts = schemas.SDailyTaskStateCreate(**i)
            await crud.dailytaskstate.create(db, userid, obj_in=sc_dts)
        except Exception:
            print(f"Can't create regulartaskstate: {i}")

    # Import day states
    for i in data['daystate']:
        sc_ds = schemas.SDayStateCreate(**i)
        await crud.daystate.create(db, userid, obj_in=sc_ds)

    # Import markdown
    for i in data['markdown']:
        uid = i["uid"]
        del i["uid"]
        sc_md = schemas.SMarkdownCreate(**i)
        obj_md = await crud.markdown.create(db, userid, obj_in=sc_md)
        map_markdown[uid] = obj_md.uid

    # Import tasklists
    for i in data['jsondoc']:
        try:
            if i["doctype"] != "tasklist":
                continue
            uid = i["uid"]
            del i["uid"]
            # Replace uid for daily state and dailytask:
            temp_jd = json.loads(i["jsondoc"])
            for j in temp_jd:
                if "type" in j and j["type"] == "regulartask":
                    j["regulartask"] = map_regulartask[j["regulartask"]]
                elif "type" in j and j["type"] == "dailytask":
                    j["dailytask"] = map_dailytask[j["dailytask"]]
            i["jsondoc"] = json.dumps(temp_jd, default=str, ensure_ascii=False)
            sc_jd = schemas.SJSONDocCreate(**i)
            obj_jd = await crud.jsondoc.create(db, userid, obj_in=sc_jd)
            map_jsondoc[uid] = obj_jd.uid
        except Exception:
            print(f"Can't create tasklist: { i }")

    # Import workspaces
    for i in data['jsondoc']:
        try:
            if i["doctype"] != "workspace":
                continue
            uid = i["uid"]
            del i["uid"]
            # Replace uid for markdown:
            temp_jd = json.loads(i["jsondoc"])
            for j in temp_jd["content"]:
                for k in j["content"]:
                    if k["type"] == "markdown":
                        k["uid"] = map_markdown[k["uid"]]
            i["jsondoc"] = json.dumps(temp_jd, default=str, ensure_ascii=False)
            sc_jd = schemas.SJSONDocCreate(**i)
            obj_jd = await crud.jsondoc.create(db, userid, obj_in=sc_jd)
            map_jsondoc[uid] = obj_jd.uid
        except Exception:
            print(f"Can't create workspace: {i}")

    # Import activity
    for i in data['jsondoc']:
        try:
            if i["doctype"] != "activity":
                continue
            uid = i["uid"]
            del i["uid"]
            # Replace uid for workspaces:
            temp_jd = json.loads(i["jsondoc"])
            for j in range(len(temp_jd["workspaces"])):
                temp_jd["workspaces"][j] = map_jsondoc[temp_jd["workspaces"][j]]
            i["jsondoc"] = json.dumps(temp_jd, default=str, ensure_ascii=False)
            sc_jd = schemas.SJSONDocCreate(**i)
            obj_jd = await crud.jsondoc.create(db, userid, obj_in=sc_jd)
            map_jsondoc[uid] = obj_jd.uid
        except Exception:
            print(f"Can't create activity: {i}")

    obj_upd = {
        "coreactivity": map_jsondoc[data["coreactivity"]],
        "coretasklist": map_jsondoc[data["coretasklist"]],
    }
    return await crud.user.update_byobj(db=db, db_obj=db_obj, obj_in=obj_upd)
