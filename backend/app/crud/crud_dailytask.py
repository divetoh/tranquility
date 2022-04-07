from app.crud.base import CRUDBaseAuth
from app.models.dailytask import DailyTask
from app.schemas import SDailyTaskCreate, SDailyTaskUpdate


class CRUDDailyTask(CRUDBaseAuth[DailyTask, SDailyTaskCreate, SDailyTaskUpdate]):
    pass


dailytask = CRUDDailyTask(DailyTask)
