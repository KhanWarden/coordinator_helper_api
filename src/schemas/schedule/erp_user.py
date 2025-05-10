import datetime
from pydantic import BaseModel


class ScheduleSchema(BaseModel):
    date: datetime.date  # YYYY-MM-DD


class ErpUserSchema(BaseModel):
    token: str
    cabinet_id: int
