import timeit

setup = """
from metricspaces import MetricSpace
from greedypermutation.clarksongreedy import greedy
from random import randrange, randint

class Point():
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        return list(self) == list(other)

    def __hash__(self):
        return hash((self.x, self.y))

def naiveDirectedHD(A: MetricSpace, B: MetricSpace, cmax: float = 0):
    for a in A:
        cmin = float('inf')
        cont = True
        for b in B:
            d = A.distfn(a,b)
            if d < cmax:
                cont = False
                break
            if d < cmin:
                cmin = d
        if cont and cmin > cmax:
            cmax = cmin
    return cmax

def naiveHD(A: MetricSpace, B: MetricSpace, cmax: float = 0):
    return max(naiveDirectedHD(A, B, cmax), naiveDirectedHD(B, A, cmax))

def greedyHD(A: MetricSpace, B: MetricSpace):
    A_g = MetricSpace(points = list(greedy(A)), dist = A.distfn, cache = A.cache, turnoffcache = A.turnoffcache)
    B_g = MetricSpace(points = list(greedy(B)), dist = B.distfn, cache = B.cache, turnoffcache = B.turnoffcache)
    return naiveHD(A_g, B_g)

def l_inf(p: Point, q: Point):
    return max(abs(p.x - q.x), abs(p.y - q.y))

M = 1000
N = 150000
n = 15
# seed(0)

# Create a random set of points without any duplicates and only 1 point on the diagonal, (0,0)

points = [Point(randrange(5, M-5), randrange(5,M-5)) for i in range(N)]
# points = [i for i in points if i.x != i.y]
# points.append(Point(0,0))
points = list(dict.fromkeys(points))

X = MetricSpace(points = points, dist=l_inf)
A = X[:N//2]
B = X[N//2:]
"""

print(timeit.timeit(stmt="naiveHD(A,B)", setup=setup, number = 100))

print(timeit.timeit(stmt="greedyHD(A,B)", setup=setup, number=100))