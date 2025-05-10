import json
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query

from src.db.mongodb.service import save_schedule_data
from src.schemas.schedule import GameShortSchema, ScheduleRequestSchema
from src.services.erp_crawler import ErpCrawler

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)


@router.get("/{schedule_date}")
async def get_schedule(
    schedule_date: date,
    erp: ErpCrawler = Depends()
) -> List[GameShortSchema]:
    data = await erp.get_schedule(date_=schedule_date)
    print(data)
    schedule: list = data.get("data")
    games = [
        GameShortSchema.model_validate(game)
        for game in schedule
        if game.get("status_id") not in {3, 5}
    ]
    return games


@router.post("/")
async def save_schedule(payload: ScheduleRequestSchema):
    schedule_id = await save_schedule_data(payload)
    return {"success": True, "id": schedule_id}
