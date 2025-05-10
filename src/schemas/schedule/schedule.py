from datetime import datetime, timedelta, date

from pydantic import BaseModel, field_validator, model_validator
from typing import Dict, Any, Optional


class GameShortSchema(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    catalog: str
    parameter_values: Dict[str, Any]

    @field_validator("start_time", "end_time", mode="before")
    def shift_time(cls, value: datetime | str) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value + timedelta(hours=5)

    @field_validator("catalog", mode="before")
    def get_catalog(cls, value: Dict[str, Any]) -> str:
        return value.get("title")


class TeamStaffSchema(BaseModel):
    host: str
    dj: str
    cohost: Optional[str]


class TeamDataSchema(BaseModel):
    games: Dict[str, str]
    staff: TeamStaffSchema


class ScheduleRequestSchema(BaseModel):
    date: date
    teams: Dict[str, TeamDataSchema]

    def to_json(self):
        return self.model_dump_json()
