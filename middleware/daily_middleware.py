import json
import time

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from service.visualcrossing_service import visualcrossing_service
from redis_base import get_data_from_redis, client
from schema.daily_schema import DailyBase

async def redis_daily_stats(request: Request, call_next):
    if request.url.path.startswith("/api/daily") and request.method == 'POST':
        byte_body = await request.body()
        if not byte_body:
            raise HTTPException(status_code=400, detail="Empty request body")

        try:
            body = json.loads(byte_body)
        except json.decoder.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        api_in = DailyBase(**body)
        redis_result = get_data_from_redis(api_in)
        start_time = time.time()
        result = {}

        for city in redis_result.keys():
            result[city] = redis_result[city]
        if len(result.keys()) == len(api_in.cities):
            return await call_next(request)
        # 将redis中没有的记录加入
        api_in.cities = [city for city in api_in.cities if city not in result.keys()]
        print(f"{api_in.cities} are not in the database")
        data = {city: await visualcrossing_service.get_weather_by_location(city, api_in.date_range) for city in api_in.cities}
        for city, stats in data.items():
            client.set(f'{stats["address"]}:{stats["days"][0]["datetime"]}', json.dumps(stats), ex=60*60*24)
        print(f"spend {(time.time() - start_time):.3f} seconds using API")
        return await call_next(request)
    else:
        return await call_next(request)


async def streaming_response_dealer(response):
    full_body = b''
    async for chunk in response.body_iterator:
        full_body += chunk
    return json.loads(full_body)
