import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(cords: tuple) -> tuple:
    params = {
        "latitude": cords[0],
        "longitude": cords[1],
        "current": "temperature_2m",
        "timezone": "auto"
    }
    response = openmeteo.weather_api(WEATHER_URL, params=params)[0]
    current = response.Current()
    time = pd.to_datetime(current.Time(), unit='s')
    time += pd.Timedelta(seconds=response.UtcOffsetSeconds())
    current_temperature = current.Variables(0).Value()
    return str(time), int(current_temperature)


# Getting weather forecast
def get_forecast(cords: tuple) -> list:
    params = {
        "latitude": cords[0],
        "longitude": cords[1],
        "hourly": ["temperature_2m", "precipitation"],
        "timezone": "auto"
    }
    response = openmeteo.weather_api(WEATHER_URL, params=params)[0]
    hourly = response.Hourly()
    hourly_temperature = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s")+pd.Timedelta(seconds=response.UtcOffsetSeconds()),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s")+pd.Timedelta(seconds=response.UtcOffsetSeconds()),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature": [int(temp) for temp in hourly_temperature],
    "precipitation": hourly_precipitation}

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe = hourly_dataframe.to_dict('records')
    forecast = [list(row.values()) for row in hourly_dataframe]
    return forecast
