class Point:
    """A simple class to describe points in Euclidean space with float
    coordinates.
    """

    def __init__(self, coords):
        self._p = tuple(float(x) for x in coords)

    @staticmethod
    def fromstring(s):
        return Point(x for x in s.split())

    def dist(self, other):
        """Compute the Euclidean distance between the `self` and `other`.
        If the dimensions don't match the distance is computed in projection
        down to the common subspace.
        """
        return (sum((a-b)**2 for (a,b) in zip(self, other))) ** (0.5)

    def __eq__(self, other):
        return self._p == other._p

    def __hash__(self):
        return hash(self._p)

    def __iter__(self):
        return iter(self._p)

    def __str__(self):
        return "(" + ", ".join(str(c) for c in self._p) +  ")"

    def __len__(self):
        return len(self._p)

if __name__ == '__main__':
    p = Point([0,0])
    q = Point.fromstring('3.3 4.4')
    print(p.dist(q))
    print(q)
