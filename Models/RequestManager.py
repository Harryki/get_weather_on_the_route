import requests
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import settings


class RequestManager:
    def __init__(self):
        self.directionsData = []
        self.weatherData = []
        pass

    def routesFromGoogle(self, origin: str, destination: str):
        # api-endpoint
        URL = "https://maps.googleapis.com/maps/api/directions/json"
        PARAMS = {
            "origin": origin,
            "destination": destination,
            "key": settings.GOOGLE_DIRECTION_API_KEY,
        }
        r = requests.get(url=URL, params=PARAMS)
        self.directionsData = r.json()
        if self.directionsData["status"] == "OK":
            return self.directionsData["routes"][0]["legs"][0]["steps"]
        return

    def getWeathers(self, locations):
        # this will enable multithreading
        with PoolExecutor(max_workers=10) as executor:
            return zip(locations, executor.map(self.weatherFromHere, locations))

    def weatherFromHere(self, location: (str, str)):
        URL = "https://weather.ls.hereapi.com/weather/1.0/report.json"
        latitude = location[0]
        longitude = location[1]
        PARAMS = {
            "apiKey": settings.HERE_API,
            "product": "observation",
            "latitude": latitude,
            "longitude": longitude,
            "oneobservation": "true",
        }
        r = requests.get(url=URL, params=PARAMS)
        if r.ok:
            return r.json()

