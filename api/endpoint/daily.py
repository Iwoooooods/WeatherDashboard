from fastapi import APIRouter
from service.visualcrossing_service import visualcrossing_service

from service.dashboard_service import dashboard_service

from schema.daily_schema import DailyBase

router = APIRouter()
@router.post("/daily_dashboard") # 展示当日多个城市的统计数据看板
async def daily_dashboard(api_in: DailyBase):
    return dashboard_service.get_daily_dashboard(api_in)

@router.get("/hourly_detail/{city_name}")
async def hourly_detail(city_name: str):
    api_in = DailyBase(cities=[city_name])
    return dashboard_service.get_hourly_dashboard(api_in)