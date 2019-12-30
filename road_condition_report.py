import requests
from geopy.distance import geodesic
from xml.etree import ElementTree
import html2text
from Models import Path, RequestManager

route_map = {
    "WA-542": "Mt. Baker Hwy SR542",
    "WA-20": "North Cascades Hwy SR20",
}

rss_map = {
    "Mt. Baker Hwy SR542": "https://www.wsdot.wa.gov/traffic/rssfeeds/baker/",
    "North Cascades Hwy SR20": "https://www.wsdot.wa.gov/traffic/rssfeeds/cascade/",
}


mtBaker = (48.859200, -121.662235)
RADIUS = 30.0


r = RequestManager()
routes = r.routesFromGoogle(
    "10715 NE 37th ct, Kirkland, WA 98033", "48.85627,-121.6691"
)
if routes:
    steps_html = []

    for step in routes:
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
        if milesFromMountain <= RADIUS:
            bar = p.description.split("<b>")
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
