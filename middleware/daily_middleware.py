import json
import time

from starlette.requests import Request
from starlette.responses import JSONResponse

from redis_base import get_data_from_redis
from schema.daily_schema import DailyBase

async def redis_daily_stats(request: Request, call_next):
    if request.url.path.startswith("/api/daily"):
        byte_body = await request.body()
        body = json.loads(byte_body)
        api_in = DailyBase(**body)
        redis_result = get_data_from_redis(api_in)
        start_time = time.time()
        result = {}
        for city in redis_result.keys():
            result[city] = redis_result[city]
        if len(result.keys()) == len(api_in.cities):
            return JSONResponse(result, status_code=200)
        body["cities"] = [city for city in api_in.cities if city not in result.keys()]
        request._body = json.dumps(body).encode("utf-8")
        response = await call_next(request)
        if hasattr(response, 'body_iterator'):
            data = streaming_response_dealer(response)
        print(f"spend {(time.time() - start_time):.3f} seconds using API")
        for city in data.keys():
            result[city] = data[city]
        return JSONResponse(result, status_code=200)
    else:
        return await call_next(request)

async def streaming_response_dealer(response):
    full_body = b''
    async for chunk in response.body_iterator:
        full_body += chunk
    return json.loads(full_body)
