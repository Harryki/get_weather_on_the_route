import requests


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

    def weatherFromHere(self, location: (str, str)):
        API_KEY = "ctFcXUL2CUkSABzCO4rhGwxrJlt-Bxx90u2SS1LuN7g"
        URL = "https://weather.ls.hereapi.com/weather/1.0/report.json"

        latitude = location[0]
        longitude = location[1]
        # latitude = "47.643059"
        # longitude = "-122.196539"

        PARAMS = {
            "apiKey": API_KEY,
            "product": "observation",
            "latitude": latitude,
            "longitude": longitude,
            "oneobservation": "true",
        }
        # p1 = (47.643059, -122.196539)
        # p2 = (47.632880, -122.185400)

        r = requests.get(url=URL, params=PARAMS)
        print(r.json())

    # defining a params dict for the parameters to be sent to the API

