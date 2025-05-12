from datetime import datetime, timedelta, date

from pydantic import BaseModel, field_validator
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
    host: Optional[str] = None
    dj: Optional[str] = None
    cohost: Optional[str] = None


class SchedulePayloadSchema(BaseModel):
    date: str
    teams: Dict[str, TeamStaffSchema]

    @field_validator("date", mode="before")
    def covert_date_to_str(cls, value) -> str:
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, str):
            try:
                parsed = date.fromisoformat(value)
                return parsed.isoformat()
            except ValueError:
                raise ValueError(
                    f"Invalid date string: {value!r}. Must be in YYYY-MM-DD format."
                )
        raise TypeError(
            f"Invalid type for date: {type(value).__name__}. Expected str or date."
        )
