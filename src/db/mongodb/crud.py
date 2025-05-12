import logging
from datetime import date
from typing import List

from src.db.mongodb.client import get_teams_collection, get_schedules_collection
from src.schemas.schedule import SchedulePayloadSchema, GameShortSchema


async def save_teams_by_date(schedule: SchedulePayloadSchema) -> None:
    collection = get_teams_collection()
    await collection.update_one(
        {"date": schedule.date},
        {"$set": schedule.model_dump()},
        upsert=True,
    )


async def get_teams_by_date(target_date: date) -> SchedulePayloadSchema | None:
    collection = get_teams_collection()
    result = await collection.find_one({"date": target_date.isoformat()})
    if result:
        return SchedulePayloadSchema(**result)
    return None


async def save_schedule_by_date(
    target_date: date, games: List[GameShortSchema]
) -> None:
    collection = get_schedules_collection()
    games_data = [game.model_dump() for game in games]

    await collection.update_one(
        {"date": target_date.isoformat()},
        {"$set": {"schedule": games_data}},
        upsert=True,
    )
    logging.info(f"Updated schedule for {target_date}")


async def get_schedule_by_date(target_date: date) -> List[GameShortSchema] | None:
    collection = get_schedules_collection()
    result = await collection.find_one({"date": target_date.isoformat()})
    if result:
        return [GameShortSchema(**game) for game in result.get("schedule", [])]
    return None
