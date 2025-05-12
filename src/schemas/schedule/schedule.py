from datetime import datetime, timedelta, date

from pydantic import BaseModel, field_validator, model_validator
from typing import Dict, Any, Optional


class GameShortSchema(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    catalog: str  # Команда
    title: Optional[str]
    parameter_values: Dict[str, Any]

    @field_validator("start_time", "end_time", mode="before")
    def shift_time(cls, value: datetime | str) -> datetime:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value + timedelta(hours=5)

    @field_validator("title", mode="before")
    def get_arriva_if_exists(cls, value: str) -> str | None:
        lower = value.lower()
        if "аррива" in lower or "арива" in lower:
            return "аррива"
        return None

    @field_validator("catalog", mode="before")
    def get_catalog(cls, value: Dict[str, Any]) -> str:
        return value.get("title")


class TeamStaffSchema(BaseModel):
    host: Optional[str]
    dj: Optional[str]
    cohost: Optional[str]


class SchedulePayloadSchema(BaseModel):
    date: date
    teams: Dict[str, TeamStaffSchema]
