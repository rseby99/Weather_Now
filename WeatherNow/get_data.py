import requests
import math
from datetime import date


def get_data(city, country, unit):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q":f"{city},{country}","units":f"{unit}"}
    

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "b9ac356800mshf0da663a66d341bp12b8e4jsn145828c1f17e"
        }
     
    response = requests.request("GET", url, headers=headers, params=querystring).json()


    weather_data = {'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                    'temp': math.floor(response['main']['temp']),
                    'temp_feels_like':math.floor(response['main']['feels_like']),
                    'temp_min':math.floor(response['main']['temp_min']),
                    'temp_max':math.floor(response['main']['temp_max']),
                    'pressure': response['main']['pressure'],
                    'humidity': response['main']['humidity'],
                    'wind_speed': response['wind']['speed'],
                    'country': response['sys']['country'],
                    'city': response['name'],
                    'code': response['cod'],
                    'date': date.fromtimestamp(response['dt']).strftime("%m/%d/%Y")
                    }

    
    
    return weather_data

def get_data_7days(city, country, unit):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

    querystring = {"q":f"{city},{country}","units":f"{unit}"}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "b9ac356800mshf0da663a66d341bp12b8e4jsn145828c1f17e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    weather_data = {"code": response['cod'],
                    "city": response['city']['name'],
                    "country" : response['city']['country'],
                    "weather" : []}

    for i in range(0,7):
        weather_data["weather"].append({
            'description': response['list'][i]['weather'][0]['description'],
            'icon': response['list'][i]['weather'][0]['icon'],
            'temp_day': math.floor(response['list'][i]['temp']['day']),
            'temp_day_max': math.floor(response['list'][i]['temp']['max']),
            'temp_day_min': math.floor(response['list'][i]['temp']['min']),
            'temp_night': math.floor(response['list'][i]['temp']['night']),
            'temp_feels_like_day':math.floor(response['list'][i]['feels_like']['day']),
            'temp_feels_like_night':math.floor(response['list'][i]['feels_like']['night']),
            'pressure': response['list'][i]['pressure'],
            'humidity': response['list'][i]['humidity'],
            'wind_speed': response['list'][i]['speed'],
            'date':date.fromtimestamp(response['list'][i]['dt']).strftime("%m/%d/%Y")
            })

    return weather_data






