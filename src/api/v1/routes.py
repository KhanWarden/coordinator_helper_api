from fastapi import APIRouter
from .endpoints.reports import router as reports_router
from .endpoints.schedule import router as schedule_router

routers = APIRouter()
router_list = [reports_router,
               schedule_router,]

for router in router_list:
    routers.include_router(router)
