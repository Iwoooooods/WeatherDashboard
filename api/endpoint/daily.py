from fastapi import APIRouter
from service.visualcrossing_service import visualcrossing_service

from schema.daily_schema import DailyBase
from utils.decorator import timer

router = APIRouter()
@router.post("/daily_dashboard") # 展示当日多个城市的统计数据看板
async def daily_dashboard(api_in: DailyBase):
    date_range = api_in.date_range
    return {city: await visualcrossing_service.get_weather_by_location(city, date_range) for city in api_in.cities}