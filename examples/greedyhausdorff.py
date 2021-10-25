"""
This is an example where greedy permutations are used to improve the naive Hausdorff distance algorithm.
When computing the Hausdorff distance between 2 pointsets one of the most popular heuristic is to use
a random ordering of points and an early break.
This is an attempt to check if using a greedy ordering instead helps improve performance.
"""

from metricspaces import MetricSpace
from greedypermutation.clarksongreedy import greedy
from greedypermutation import Point
from random import randrange, seed

def naiveDirectedHD(A: MetricSpace, B: MetricSpace, cmax: float = 0):
    """
    Compute directed Hausdorff distance naively in O(n^2) time.
    """
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
    """
    Compute the Hausdorff distance naively using 2 calls to naiveDirectedHD
    """
    return max(naiveDirectedHD(A, B, cmax), naiveDirectedHD(B, A, cmax))

def greedyHD(A: MetricSpace, B: MetricSpace):
    """
    Compute Hausdorff distance after taking greedy permutations of A and B.
    """
    A_g = MetricSpace(points = list(greedy(A)), dist = A.distfn, cache = A.cache, turnoffcache = A.turnoffcache)
    B_g = MetricSpace(points = list(greedy(B)), dist = B.distfn, cache = B.cache, turnoffcache = B.turnoffcache)
    return naiveHD(A_g, B_g)

def l_inf(p: Point, q: Point):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]))

M = 300
N = 350
seed(0)

points = [Point([randrange(5, M-5), randrange(5,M-5)]) for i in range(N)]
points = list(dict.fromkeys(points))

X = MetricSpace(points = points, dist=l_inf)
A = X[:N//2]
B = X[N//2:]

print(naiveHD(A, B))

print(greedyHD(A, B))