class MetricSpace:
    def __init__(self, points = ()):
        self._points = list(points)

    def dist(self, a, b):
        return a.dist(b)

    def _swap(self, i, j):
        self._points[i], self._points[j] = self._points[j], self._points[i]

    def greedytree(self, seed = None):
        # If no seed is provided, use the first point.
        if seed is None:
            seed = self._points[0]
        # Put the seed in the first position.
        self._swap(self._points.index(seed), 0)
        P = self._points
        n = len(P)
        yield P[0], None
        pred = {p:P[0] for p in P}
        preddist = {p: self.dist(p, pred[p]) for p in P}
        for i in range(1,n):
            farthest = i
            for j in range(i+1, n):
                if preddist[P[j]] > preddist[P[farthest]]:
                    farthest  = j
            self._swap(i, farthest)
            # Update the predecessor distance if necessary.
            for j in range(i+1, n):
                newdistance = self.dist(P[i], P[j])
                if newdistance < preddist[P[j]]:
                    pred[P[j]] = P[i]
                    preddist[P[j]] = newdistance
            yield P[i], pred[P[i]]


    def __iter__(self):
        return iter(self._points)

    def __len__(self):
        return len(self._points)

if __name__ == '__main__':
    from point import Point
    P = [Point(a,b) for (a,b) in [(1,2), (2,3),(0,20), (3,100)]]
    X = MetricSpace(P)
    for p, pred in X.greedytree():
        print(str(p))
