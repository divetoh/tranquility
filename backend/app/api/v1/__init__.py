from fastapi import APIRouter

from . import dailytask
from . import dailytaskstate
from . import daystate
from . import jsondoc
from . import login
from . import markdown
from . import regulartask
from . import regulartaskstate
from . import users


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(jsondoc.router, prefix="/jsondoc", tags=["jsondoc"])
api_router.include_router(markdown.router, prefix="/markdown", tags=["markdown"])
api_router.include_router(regulartask.router, prefix="/regulartask", tags=["regulartask"])
api_router.include_router(dailytask.router, prefix="/dailytask", tags=["dailytask"])

api_router.include_router(daystate.router, prefix="/daystate", tags=["states"])
api_router.include_router(regulartaskstate.router, prefix="/regulartaskstate", tags=["states"])
api_router.include_router(dailytaskstate.router, prefix="/dailytaskstate", tags=["states"])
