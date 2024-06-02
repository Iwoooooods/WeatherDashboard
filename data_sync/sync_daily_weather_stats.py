import json
import asyncio
import threading

from typing import List
from datetime import date

from redis_base import client
from utils.decorator import timer
from service.visualcrossing_service import visualcrossing_service
from utils.constant import default_cities

daily_expire = 60 * 60 * 24
date_range = {'start_date': date.today(), 'end_date': date.today()}

async def fetch_daily_weather_stats(cities: List[str]):
    tasks = [visualcrossing_service.get_weather_by_location(city, date_range) for city in cities]
    return await asyncio.gather(*tasks)

def set_stats_dict(total_stats: List[dict]):
    stats_dict = {}
    for city_stats in total_stats:
        city_name = city_stats['address']
        stats_dict[city_name] = city_stats
    return stats_dict

def sync_stats_dict(city_stats, city_name: str):
    """
    :param city_stats:{
        'New York': [
            {
                'date_time': xxx,
                ...
            },
            ...
        ]
    }
    :return:
    """
    date_time = city_stats['days'][0]['datetime']
    # print(stats)
    client.set(f'{city_name}:{date_time}', json.dumps(city_stats), ex=daily_expire)
    print(f"successfully set {city_name}:{date_time}")

@timer
def sync_daily_weather_stats(stats_dict: dict):
    for city_name, stats in stats_dict.items():
        sync_stats_dict(stats, city_name)

async def main():
    while True:
        total_stats = await fetch_daily_weather_stats(default_cities)
        stats_dict = set_stats_dict(total_stats)
        sync_daily_weather_stats(stats_dict)


# if __name__ == '__main__':
#     total_stats = asyncio.run(fetch_daily_weather_stats(default_cities))
#     stats_dict = set_stats_dict(total_stats)
#     sync_daily_weather_stats(stats_dict)


sleep_time = 60*60*24
t = threading.Thread(target=main)
t.daemon = True
t.start()