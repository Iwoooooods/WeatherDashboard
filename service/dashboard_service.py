
from redis_base import client, get_data_from_redis
from schema.daily_schema import DailyBase


class DashboardService:
    def get_daily_dashboard(self, api_in: DailyBase) -> dict:
        stats_dict = {}
        city_stats = get_data_from_redis(api_in)
        for city in api_in.cities:
            temp_dict = {}
            total_stats = city_stats[city]
            daily_stats = total_stats['days'][0]
            temp_dict['position'] = {'latitude': total_stats['latitude'], 'longitude': total_stats['longitude']}
            temp_dict['temperature'] = daily_stats['temp']
            temp_dict['feels_like'] = daily_stats['feelslike']
            temp_dict['dew'] = daily_stats['dew']
            temp_dict['humidity'] = daily_stats['humidity']
            temp_dict['preciptype'] = daily_stats['preciptype']
            temp_dict['snow'] = daily_stats['snow']
            temp_dict['windspeed'] = daily_stats['windspeed']
            temp_dict['pressure'] = daily_stats['pressure']
            temp_dict['cloudcover'] = daily_stats['cloudcover']
            temp_dict['solarradiation'] = daily_stats['solarradiation']
            temp_dict['sunset'] = daily_stats['sunset']
            temp_dict['description'] = daily_stats['description']

            stats_dict[city] = temp_dict
        return stats_dict

    def get_hourly_dashboard(self, api_in):
        total_stats = get_data_from_redis(api_in)
        hourly_stats = total_stats[api_in.cities[0]]['days'][0]['hours']
        return hourly_stats

dashboard_service = DashboardService()