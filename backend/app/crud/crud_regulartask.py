from app.crud.base import CRUDBaseAuth
from app.models.regulartask import RegularTask
from app.schemas import SRegularTaskCreate, SRegularTaskUpdate


class CRUDRegularTask(CRUDBaseAuth[RegularTask, SRegularTaskCreate, SRegularTaskUpdate]):
    pass


regulartask = CRUDRegularTask(RegularTask)
