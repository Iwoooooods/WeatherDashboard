from fastapi import FastAPI
from api.api import router

from middleware.daily_middleware import redis_daily_stats

app = FastAPI()
app.include_router(router, prefix="/api", tags=[""])
app.middleware("http")(redis_daily_stats)

@app.get("/")
async def root():
    return {"message": "Welcome to WeatherAPIWrapperService"}

