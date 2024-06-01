import json

import redis
from datetime import timedelta
from schema.daily_schema import DailyBase
from utils.decorator import timer

client = redis.Redis(host='localhost', port=6379, db=0)

@timer
def get_data_from_redis(api_in: DailyBase):
    delta = (api_in.date_range['end_date'] - api_in.date_range['start_date']).days
    keys = []
    for i in range(delta+1):
        temp_keys = [f"{city}:{api_in.date_range['start_date'] + timedelta(days=i)}" for city in api_in.cities]
        keys.extend(temp_keys)
    result = {key[:-11]: client.get(key) for key in keys}
    return {key: json.loads(value) for key, value in result.items() if value is not None}

if __name__ == '__main__':
    print(get_data_from_redis(DailyBase()))
