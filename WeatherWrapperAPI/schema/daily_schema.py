from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from utils.constant import default_cities

class DailyBase(BaseModel):
    cities: Optional[List] = default_cities
    date_range: Optional[dict] = {'start_date': date.today(), 'end_date': date.today()}

if __name__ == '__main__':
    print((date(2024,6,1) - date(2024,5,31)).days)