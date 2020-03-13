class MetricSpace:
    def __init__(self, points = ()):
        self._points = set(points)

    def add(self, point):
        self._points.add(point)

    def fromstrings(self, strings, parser):
        for s in strings:
            self.add(parser(s.split(';')[0]))

    def dist(self, a, b):
        return a.dist(b)

    def __iter__(self):
        return iter(self._points)

    def __len__(self):
        return len(self._points)

if __name__ == '__main__':
    pass
