# import requests
from geopy.distance import geodesic
from Models import Path, RequestManager
from collections import deque
import time
import json

r = RequestManager()
routes = r.routesFromGoogle(
    "10715 NE 37th ct, Kirkland, WA 98033", "48.85627,-121.6691"
)
if routes:
    steps_html = deque()
    locations = []
    for step in routes:
        start = (step["start_location"]["lat"], step["start_location"]["lng"])
        end = (step["end_location"]["lat"], step["end_location"]["lng"])
        description = step["html_instructions"]
        roadDistance = step["distance"]["value"]
        p = Path(start, end, roadDistance, description)

        # append it to the stack
        steps_html.append(p)

    cur, prev = None, None
    while steps_html:
        p = steps_html.popleft()

        if prev is None:
            cur, prev = p, p
            locations.append(cur.start)
        else:
            cur = p
        singleDistance = geodesic(cur.start, cur.end).miles
        distance = geodesic(prev.start, cur.start).miles

        THRESHOLD = 20.0
        if singleDistance >= THRESHOLD:  # IMPROVE: add altitude as a condition
            midPoints = cur.getMidPoints(THRESHOLD)
            locations.extend(midPoints)

        if distance >= THRESHOLD:
            prev = cur
            locations.append(cur.start)

    locations.extend([cur.start, cur.end])

    ##### this was speed test to see if threading actually works #####
    # start = time.time()
    # for location in locations:
    #     data = r.weatherFromHere(location)
    #     print(data)
    # end = time.time()
    # print(end - start)

    # start = time.time()
    res = r.getWeathers(locations)
    for location, data in list(res):
        # print(location, data)
        print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        # pass
    # end = time.time()
    # print(end - start)

