from fastapi import APIRouter

from api.endpoint import daily, login

router = APIRouter()

router.include_router(daily.router, prefix='/daily', tags=["daily_statistics"])
router.include_router(login.router, prefix='/auth', tags=["authorization"])