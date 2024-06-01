from fastapi import APIRouter

from api.endpoint import daily

router = APIRouter()

router.include_router(daily.router, prefix='/daily', tags=["daily_statistics"])