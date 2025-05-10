from fastapi import APIRouter


router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.post("/")
async def create_report():
    pass
