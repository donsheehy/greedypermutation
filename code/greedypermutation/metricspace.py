class MetricSpace:
    def __init__(self, points = ()):
        self._points = list(points)

    def add(self, point):
        self._points.append(point)

    def fromstrings(self, strings, parser):
        for s in strings:
            self.add(parser(s.split(';')[0]))

    def dist(self, a, b):
        return a.dist(b)

    def _swap(self, i, j):
        self._points[i], self._points[j] = self._points[j], self._points[i]

    # def greedy(self, seed = None):
    #     for p, i in self.greedytree(seed):
    #         yield p
    #
    # def greedytree(self, seed = None):
    #     # If no seed is provided, use the first point.
    #     if seed is None:
    #         seed = self._points[0]
    #     # Put the seed in the first position.
    #     self._swap(self._points.index(seed), 0)
    #     P = self._points
    #     n = len(P)
    #     yield P[0], 0
    #     pred = {p:0 for p in P}
    #     preddist = {p: self.dist(p, P[pred[p]]) for p in P}
    #     for i in range(1,n):
    #         farthest = i
    #         for j in range(i+1, n):
    #             if preddist[P[j]] > preddist[P[farthest]]:
    #                 farthest  = j
    #         self._swap(i, farthest)
    #         # Update the predecessor distance if necessary.
    #         for j in range(i+1, n):
    #             newdistance = self.dist(P[i], P[j])
    #             if newdistance < preddist[P[j]]:
    #                 pred[P[j]] = i
    #                 preddist[P[j]] = newdistance
    #         yield P[i], pred[P[i]]

    def __iter__(self):
        return iter(self._points)

    def __len__(self):
        return len(self._points)

if __name__ == '__main__':
    pass
