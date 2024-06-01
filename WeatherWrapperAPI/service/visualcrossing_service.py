import time

import requests

from fastapi import HTTPException
from typing import Optional, Dict

api_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
api_key = 'MP9RAXR7G9Z4798VNHYAKZN8X'

class VisualCrossingService:
    def __init__(self):
        self.api_url = api_url
        self.api_key = api_key

    async def get_weather_by_location(self, location: str, date_range: Optional[Dict] = None) -> dict:
        if date_range:
            start_date = date_range['start_date']
            end_date = date_range['end_date']
            response = requests.get(f"{self.api_url}{location}/{start_date}/{end_date}?key={api_key}&contentType=json")
        else:
            response = requests.get(f"{api_url}{location}?key={api_key}&contentType=json")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise HTTPException(status_code=404, detail=response.text)
        else:
            raise HTTPException(status_code=500, detail=response.text)

    async def get_weather_by_position(self, longitude: float, latitude: float, date_range: Optional[Dict] = None) -> dict:
        if date_range:
            start_date = date_range['start_date']
            end_date = date_range['end_date']
            response = requests.get(f"{self.api_url}{latitude},{longitude}/{start_date}/{end_date}?key={api_key}&contentType=json")
        else:
            response = requests.get(f"{self.api_url}{latitude},{longitude}?key={api_key}&contentType=json")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise HTTPException(status_code=404, detail=response.text)
        else:
            raise HTTPException(status_code=500, detail=response.text)


visualcrossing_service = VisualCrossingService()

if __name__ == '__main__':
    import asyncio
    result = asyncio.run(visualcrossing_service.get_weather_by_location('Beijing'))
    for daily in result['days']:
        print(daily)

