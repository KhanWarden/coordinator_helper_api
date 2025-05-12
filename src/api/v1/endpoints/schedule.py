from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.db.mongodb import crud
from src.schemas.schedule import GameShortSchema, SchedulePayloadSchema
from src.services.erp_crawler import ErpCrawler

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)


@router.get("/{target_date}")
async def get_schedule(
    target_date: date, erp: ErpCrawler = Depends()
) -> List[GameShortSchema]:
    data = await erp.get_schedule(date_=target_date)
    schedule = data.get("data")
    games = [
        GameShortSchema.model_validate(game)
        for game in schedule
        if game.get("status_id") not in {3, 5}
    ]
    await crud.save_schedule_by_date(target_date=target_date, games=games)
    return games


@router.get("/{target_date}/teams", response_model=SchedulePayloadSchema)
async def get_schedule_teams(target_date: date) -> SchedulePayloadSchema:
    schedule_teams = await crud.get_teams_by_date(target_date)
    if not schedule_teams:
        raise HTTPException(
            status_code=404, detail=f"No teams for schedule in {target_date}"
        )
    return schedule_teams


@router.post("/")
async def save_schedule(payload: SchedulePayloadSchema):
    await crud.save_teams_by_date(payload)
    return {"success": True}
