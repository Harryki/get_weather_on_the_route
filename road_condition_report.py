import requests
from geopy.distance import geodesic
from xml.etree import ElementTree
import html2text
from Models import Path

route_map = {
    "WA-542": "Mt. Baker Hwy SR542",
    "WA-20": "North Cascades Hwy SR20",
}

rss_map = {
    "Mt. Baker Hwy SR542": "https://www.wsdot.wa.gov/traffic/rssfeeds/baker/",
    "North Cascades Hwy SR20": "https://www.wsdot.wa.gov/traffic/rssfeeds/cascade/",
}


# api-endpoint
URL = "https://maps.googleapis.com/maps/api/directions/json"

# defining a params dict for the parameters to be sent to the API
PARAMS = {
    "origin": "10715 NE 37th ct, Kirkland, WA 98033",
    "destination": "Mt Baker Hwy, Deming, WA 98244",
    "key": "AIzaSyBfLoWx-WoRR0CXlcaBfAN0zRzEXFrf21Y",
}

mtBaker = (48.859200, -121.662235)
radius = 30.0

# sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS)

# extracting data in json format
data = r.json()
# print(r.request.url)

if data["status"] == "OK":
    routes = data["routes"]
    steps_html = []
    # print("Summary:", routes[0]["summary"])

    for step in routes[0]["legs"][0]["steps"]:
        # init path object
        start = (step["start_location"]["lat"], step["start_location"]["lng"])
        end = (step["end_location"]["lat"], step["end_location"]["lng"])
        description = step["html_instructions"]
        distance = step["distance"]["value"]
        p = Path(start, end, distance, description)

        # append it to the stack
        steps_html.append(p)

    while steps_html:
        p = steps_html.pop()
        milesFromMountain = geodesic(mtBaker, p.start).miles
        roadName = ""
        if milesFromMountain <= 30:
            bar = p.description.split("<b>")
            # print(bar)
            for key in route_map.keys():
                for b in bar:
                    if key in b:
                        # found road name from desc
                        roadName = route_map[key]
                        del route_map[key]
                        break
                if roadName:
                    break
            if roadName:
                response = requests.get(url=rss_map[roadName])
                tree = ElementTree.fromstring(response.content)
                root = tree.find("channel")
                item = root.find("item")

                for i in list(item):
                    if i.tag == "description":
                        print(html2text.html2text(i.text))

else:
    print("not ok")

