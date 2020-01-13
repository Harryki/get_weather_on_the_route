def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and "message" in request.args:
        return request.args.get("message")
    elif request_json and "message" in request_json:
        return request_json["message"]
    else:
        return f"Hello World!"


def get_weathers_on_the_route(request=None, res):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    from geopy.distance import geodesic
    from Models import Path, RequestManager
    from collections import deque

    import json
    
    if request is not None:
        # PRODUCTION:
        request_json = request.get_json()
        if request_json:
            if "origin" in request_json and "destination" in request_json:
                r = RequestManager()
                routes = r.routesFromGoogle(
                    request_json["origin"], request_json["destination"]
                )
            else:
                return f"no origin or destination or both"
        else:
            return f"Hello World!"
    else:
        # DEBUG:
        r = RequestManager()
        routes = r.routesFromGoogle("kirkland Crossing", "Alki Beach",)

    if routes:
        steps_html = deque()
        locations = []
        for step in routes:
            start = (
                step["start_location"]["lat"],
                step["start_location"]["lng"],
            )
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

        if singleDistance >= THRESHOLD:
            locations.extend([cur.start, cur.end])
        else:
            locations.extend([cur.start])

        res = r.getWeathers(locations)
        res_data = [data for location, data in list(res)]
        return (json.dumps(res_data, indent=2), 200, headers)

    else:
        return f"no routes from google"


if __name__ == "__main__":
    res = get_weathers_on_the_route()
    print(res)
else:
    print("hi")
