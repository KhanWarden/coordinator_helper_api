import os
from datetime import date

from motor.motor_asyncio import AsyncIOMotorClient

from src.schemas.schedule import SchedulePayloadSchema

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(mongo_uri)
db = client["schedule_db"]
collection = db["schedules"]


async def save_schedule(schedule_data: SchedulePayloadSchema) -> str:
    schedule_dict = schedule_data.model_dump()
    result = await collection.insert_one(schedule_dict)
    return str(result.inserted_id)


async def get_schedule_by_date(schedule_date: date) -> dict | None:
    schedule = await collection.find_one({"date": schedule_date})
    return schedule if schedule else None
