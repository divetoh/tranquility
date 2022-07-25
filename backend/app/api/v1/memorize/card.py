from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps, resp

router = APIRouter()


@router.get("/", response_model=list[schemas.SMemorizeCardOut])
async def read_memorizecards(
    stack: Optional[int],
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return all Memorize Cards.
    """
    return await crud.memorizecard.get_multi(_db, _user.uid, stack=stack)


@router.get("/{uid}", response_model=schemas.SMemorizeCardOut, responses=resp.C34)
async def read_memorizecard_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Card.
    """
    return await crud.memorizecard.get(_db, _user.uid, uid=uid, r404=True)


@router.get("/{uid}/history", response_model=schemas.SMemorizeCardOutHistory, responses=resp.C34)
async def read_memorizecardhistory_by_id(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return Memorize Card History.
    """
    return await crud.memorizecardhistory.get_histroy(_db, _user.uid, card=uid)


@router.put("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def update_memorizecard(
    uid: int,
    card_in: schemas.SMemorizeCardUpdate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Memorize Card.
    """
    await crud.memorizecard.update(_db, _user.uid, uid=uid, obj_in=card_in)
    return schemas.SBoolOut(state=True)


@router.post("/", response_model=schemas.SMemorizeCardBaseOut)
async def create_memorizecard(
    card_in: schemas.SMemorizeCardCreate,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Memorize Card.
    """
    return await crud.memorizecard.create(_db, _user.uid, obj_in=card_in)


@router.delete("/{uid}", response_model=schemas.SBoolOut, responses=resp.C34)
async def delete_memorizecard(
    uid: int,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Memorize Card.
    """
    await crud.memorizecard.remove(_db, _user.uid, uid=uid)
    return schemas.SBoolOut(state=True)


@router.post("/{uid}/answer", response_model=schemas.SMemorizeAnswerOut)
async def add_memorizecard_answer(
    uid: int,
    answer_in: schemas.SMemorizeAnswerIn,
    _db: AsyncSession = Depends(deps.get_db),
    _user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Register answer.
    """
    history = await crud.memorizecardhistory.create(_db, _user.uid, card=uid, state=answer_in.state)
    state = await crud.memorizecardstate.get(_db, _user.uid, card=uid)
    if not state:
        new_state = schemas.SMemorizeStateCreate(
            state=answer_in.state,
            lastdate=answer_in.answerdate,
            nextdate=answer_in.answerdate + timedelta(days=1),
        )
        state = await crud.memorizecardstate.create(_db, _user.uid, card=uid, obj_in=new_state)
    else:
        update: dict["str", Any] = {"lastdate": answer_in.answerdate}
        if answer_in.state == 0:
            update["state"] = 0
            update["nextdate"] = answer_in.answerdate + timedelta(days=1)
        elif state.lastdate != answer_in.answerdate:
            update["state"] = state.state + 1
            update["nextdate"] = answer_in.answerdate + timedelta(days=min(update["state"]**2, 45))
        state = await crud.memorizecardstate.update_byobj(_db, _user.uid, db_obj=state, obj_in=update)
    return schemas.SMemorizeAnswerOut(history=history, state=state)
