from app import schemas
from app.crud.base import CRUDBaseAuth
from app.models import MemorizeCategory


class CRUDMemorizeCategory(CRUDBaseAuth[
    MemorizeCategory,
    schemas.SMemorizeCategoryCreate,
    schemas.SMemorizeCategoryUpdate,
]):
    pass


memorizecategory = CRUDMemorizeCategory(MemorizeCategory)
