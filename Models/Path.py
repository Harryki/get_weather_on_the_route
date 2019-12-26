from geopy.distance import geodesic


class Path:
    def __init__(self, start, end, roadDistance, description):
        self.start = start
        self.end = end
        self.roadDistance = roadDistance
        self.description = description

    def getMidPoints(self, threshold=30.00):
        res = []

        def helper(start, end, threshold, res):
            distance = geodesic(start, end).miles
            if distance < 2 * threshold:
                return
            # get mid point and call recursively
            mid = self.getMidPoint(start, end)
            res.append(mid)
            helper(start, mid, threshold, res)
            helper(mid, end, threshold, res)

        helper(self.start, self.end, threshold, res)

        # sort res based on direction
        res.sort(reverse=self.end[0] - self.start[0] < 0)
        return res

    def getMidPoint(self, origin, destination):
        lats = [origin[0], destination[0]]
        longs = [origin[1], destination[1]]
        lat = float("{0:.14f}".format(sum(lats) / 2))
        lng = float("{0:.14f}".format(sum(longs) / 2))
        return (lat, lng)

    def getGeodesicDistance(self):
        return geodesic(self.start, self.end).miles
