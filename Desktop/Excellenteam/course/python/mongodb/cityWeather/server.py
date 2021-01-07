from config import API_KEY
from flask import Flask, Response, request
import json
import requests
import  city_model

app = Flask(__name__)


@app.route('/weatherCheck/<city>')
def weather_check(city):
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY)
    city_weather = requests.get(url=weather_url).json()
    if city_weather.get("cod") != 200:
        return city_weather
# {"name": city_weather.get("name"), "temp":city_weather["main"]["temp"]}
    return json.dumps(city_weather)


@app.route('/addCity', methods = ["POST"])
def add_city():
    city_data = request.get_json()
    city_model.add_city_data(city_data)
    return json.dumps({"created": city_data["name"]})


# @app.route('/citiesWeather')
# def cities_weather():
#     res = dict()
#     all_data = city_model.get_all_cities_weather()
#     for data in all_data:
#         res[data["name"]] = data
#     return Response(json.dumps(res,  default=str))

    
# @app.route('/deleteCity/<city>', methods = ["DELETE"])
# def delete_city(city):
#     city_model.delete_city(city)
#     return json.dumps({"deleted": city})


# @app.route('/updateeCity/<city>', methods = ["POST"])
# def update_city(city):
#     city_data = request.get_json()
#     city_model.update_city(city, city_data)
#     return json.dumps({"updated": city})

    
# @app.route('/warmestCities')
# def warmest_cities():
#     res = dict()
#     warmest_cities = city_model.get_two_warmest_cities()
#     for city in warmest_cities:
#         res[city["name"]] = city["main"]["temp"]
#     return Response(json.dumps(res,  default=str))


if __name__ == '__main__':
    app.run(port = 3000)