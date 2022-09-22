import json
from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models
from app.api import deps


router = APIRouter()


@router.get("/full_json", response_class=Response, responses={200: {"content": {"application/json": {}}}})
async def read_dailytask(
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate json with all user data.
    """
    dailytask = await crud.dailytask.get_multi(_db, _user.uid)
    dailytaskstate = await crud.dailytaskstate.get_multi_bydate(
        _db,
        _user.uid,
        start=date(1980, 1, 1),
        end=date(3080, 1, 1),
    )
    daystate = await crud.daystate.get_multi_bydate(
        _db,
        _user.uid,
        start=date(1980, 1, 1),
        end=date(3080, 1, 1),
    )
    jsondoc = await crud.jsondoc.get_multi(_db, _user.uid)
    markdown = await crud.markdown.get_multi(_db, _user.uid)
    regulartask = await crud.regulartask.get_multi(_db, _user.uid)
    regulartaskstate = await crud.regulartaskstate.get_multi_bydate(
        _db,
        _user.uid,
        start=date(1980, 1, 1),
        end=date(3080, 1, 1),
    )

    memorizestack = await crud.memorizestack.get_multi(_db, _user.uid)
    memorizecategory = await crud.memorizecategory.get_multi(_db, _user.uid)
    memorizecard = await crud.memorizecard.get_multi(_db, _user.uid)
    folder = await crud.folder.get_multi(_db, _user.uid)

    archive = {
        "full_name": _user.full_name,
        "email": _user.email,
        "coretasklist": _user.coretasklist,
        "coreactivity": _user.coreactivity,
        "dailytask": [i.as_dict(exclude=["user"]) for i in dailytask],
        "dailytaskstate": [i.as_dict(exclude=["user"]) for i in dailytaskstate],
        "daystate": [i.as_dict(exclude=["user"]) for i in daystate],
        "jsondoc": [i.as_dict(exclude=["user"]) for i in jsondoc],
        "markdown": [i.as_dict(exclude=["user"]) for i in markdown],
        "regulartask": [i.as_dict(exclude=["user"]) for i in regulartask],
        "regulartaskstate": [i.as_dict(exclude=["user"]) for i in regulartaskstate],
        "memorizestack": [i.as_dict(exclude=["user"]) for i in memorizestack],
        "memorizecategory": [i.as_dict(exclude=["user"]) for i in memorizecategory],
        "memorizecard": [i.as_dict(exclude=["user"]) for i in memorizecard],
        "folder": [i.as_dict(exclude=["user"]) for i in folder],
    }

    archive_bytes = json.dumps(archive, default=str, ensure_ascii=False).encode('utf-8')
    return Response(content=archive_bytes, media_type="application/json")
