from fastapi import APIRouter

from . import (archive, dailytask, dailytaskstate, daystate, jsondoc, login,
               markdown, memorize, regulartask, regulartaskstate, users)

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

api_router.include_router(archive.router, prefix="/archive", tags=["tools"])

api_router.include_router(memorize.stack.router, prefix="/memorize/stack", tags=["memorize"])
api_router.include_router(memorize.category.router, prefix="/memorize/category", tags=["memorize"])
api_router.include_router(memorize.card.router, prefix="/memorize/card", tags=["memorize"])
