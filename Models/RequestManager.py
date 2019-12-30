import requests
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


class RequestManager:
    def __init__(self):
        self.directionsData = []
        self.weatherData = []
        pass

    def routesFromGoogle(self, origin: str, destination: str):
        # api-endpoint
        URL = "https://maps.googleapis.com/maps/api/directions/json"
        PARAMS = {
            # "origin": "10715 NE 37th ct, Kirkland, WA 98033",
            # "destination": "Mt Baker Hwy, Deming, WA 98244",
            "origin": origin,
            "destination": destination,
            "key": "AIzaSyBfLoWx-WoRR0CXlcaBfAN0zRzEXFrf21Y",
        }
        r = requests.get(url=URL, params=PARAMS)
        self.directionsData = r.json()
        if self.directionsData["status"] == "OK":
            return self.directionsData["routes"][0]["legs"][0]["steps"]
        return

    def getWeathers(self, locations):
        with PoolExecutor(max_workers=10) as executor:
            # for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            #     print("%d is prime: %s" % (number, prime))
            return zip(locations, executor.map(self.weatherFromHere, locations))

    def weatherFromHere(self, location: (str, str)):
        API_KEY = "ctFcXUL2CUkSABzCO4rhGwxrJlt-Bxx90u2SS1LuN7g"
        URL = "https://weather.ls.hereapi.com/weather/1.0/report.json"
        latitude = location[0]
        longitude = location[1]
        PARAMS = {
            "apiKey": API_KEY,
            "product": "observation",
            "latitude": latitude,
            "longitude": longitude,
            "oneobservation": "true",
        }
        r = requests.get(url=URL, params=PARAMS)
        if r.ok:
            return r.json()

    # defining a params dict for the parameters to be sent to the API

