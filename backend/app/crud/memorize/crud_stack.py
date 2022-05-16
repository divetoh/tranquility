from app import schemas
from app.crud.base import CRUDBaseAuth
from app.models import MemorizeStack


class CRUDMemorizeStack(CRUDBaseAuth[MemorizeStack, schemas.SMemorizeStackCreate, schemas.SMemorizeStackUpdate]):
    pass


memorizestack = CRUDMemorizeStack(MemorizeStack)
