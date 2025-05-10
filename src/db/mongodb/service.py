from src.db.mongodb.repository import save_schedule, get_schedule_by_date
from datetime import date

from src.schemas.schedule import ScheduleRequestSchema


async def save_schedule_data(schedule_data: ScheduleRequestSchema) -> str:
    return await save_schedule(schedule_data)


async def fetch_schedule_by_date(schedule_date: date) -> dict:
    return await get_schedule_by_date(schedule_date)
