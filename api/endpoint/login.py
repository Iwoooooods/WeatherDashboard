from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.base_mysql import get_db
from service.auth_service import auth_service

router = APIRouter()

@router.get("/login/{username}")
async def login(username: str, db: Session = Depends(get_db)):
    return auth_service.check_user_exists(username, db)