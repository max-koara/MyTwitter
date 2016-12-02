import requests
import json
import openWM

API_KEY = openWM.API
URL = "http://api.openweathermap.org/data/2.5/weather" 

r = requests.get(URL + "?q=Aizu-Wakamatsu-shi,jp&APPID=" + API_KEY)

data = r.json()


city_name = data['name']
weather = data['weather'][0]['description']
humidity = str(data['main']['humidity'])
temp = str(data['main']['temp'] - 273.15)
max_temp = str(data['main']['temp_max'] -273.15)
min_temp = str(data['main']['temp_min'] - 273.15)
pressure = str(data['main']['pressure'])
wind = str(data['wind']['speed'])

