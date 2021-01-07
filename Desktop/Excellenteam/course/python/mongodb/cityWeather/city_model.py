from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient("localhost")
db = client.weatherDB

def add_city_data(city_data):
    db.citiesCollection.insert(city_data)

def get_all_cities_weather():
    return db.citiesCollection.find({})

def delete_city(city_name):
    db.citiesCollection.remove({"name" : city_name})

def update_city(city_name, city_data):
    db.citiesCollection.update(
    {
        "name": city_name
    },
    {
        "$set": city_data
    }
)

def get_two_warmest_cities():
    return db.citiesCollection.find({},
    {"_id": 0, "name": 1, "main": 1}).sort("main.temp", DESCENDING).limit(2)