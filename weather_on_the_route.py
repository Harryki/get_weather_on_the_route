from geopy.distance import geodesic
from Models import Path, RequestManager
from collections import deque

import json

# import time

r = RequestManager()
# accept origin and destination as input
routes = r.routesFromGoogle(
    "Kirkland Library",
    "Alki Beach",
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
            # print("midpoint added")
            locations.extend(midPoints)

        if distance >= THRESHOLD:
            # print("new  cur point")
            prev = cur
            locations.append(cur.start)
    # if cur.start ~ cur.end is bigger than thresh hold, add end as well
    # locations.extend([cur.start, cur.end])
    if singleDistance >= THRESHOLD:
        locations.extend([cur.start, cur.end])
    else:
        locations.extend([cur.start])

    ##### this was speed test to see if threading actually works #####
    # start = time.time()
    # for location in locations:
    #     data = r.weatherFromHere(location)
    #     print(data)
    # end = time.time()
    # print(end - start)

    # start = time.time()

    print("***** Here's Weather Report *****\n")
    res = r.getWeathers(locations)
    for location, data in list(res):
        res_location = (
            data["observations"]["location"][0]["latitude"],
            data["observations"]["location"][0]["longitude"],
        )
        print(location, res_location)
        print(data["observations"]["location"][0]["observation"][0]["description"])
        print()
        # print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        # print(location)

        # pass
    # end = time.time()
    # print(end - start)

