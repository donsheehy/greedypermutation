class Point:
    def __init__(self, *coords):
        self._p = list(coords)

    def dist(self, other):
        return (sum(a*a + b*b for (a,b) in zip(self, other))) ** (0.5)

    def __hash__(self):
        return sum(hash(c) for c in self)

    def __iter__(self):
        return iter(self._p)

    def __str__(self):
        return "(" + ", ".join(str(c) for c in self._p) +  ")"

if __name__ == '__main__':
    p = Point(0,0)
    q = Point(3,4)
    print(p.dist(q))
    print(p)
