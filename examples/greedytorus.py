import ripser
from greedypermutation.clarksongreedy import greedy
#from metricspaces import MetricSpace
from ds2viz.element import Circle, Line
from ds2viz.canvas import svg_plus_pdf
from random import randrange, seed
from tadasets import torus
from ripser import ripser
#from persim import plot_diagrams


def _l_inf(p, q):
    return max(abs(p.x-q.x), abs(p.y-q.y))


def _proj(p):
    return Point((p.x + p.y)/2, (p.x+p.y)/2)


class Point(Circle):
    def __init__(self, x, y, radius=1):
        super().__init__(radius)
        self.x = x
        self.y = y
        self.radius = radius

    def __repr__(self) -> str:
        return("("+str(self.x)+","+str(self.y)+")")

    def dist(self, other):
        return min(_l_inf(self, other), _l_inf(self, _proj(self)) + _l_inf(other, _proj(other)))

    def __eq__(self, other):
        return list(self) == list(other)

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash((self.x, self.y))


seed(0)
scale = 10
M = 25*scale
n = 5

base_set = torus(n=200, c=2, a=1)
rips = ripser(base_set)

# print(rips['dgms'][1])
# plot_diagrams(rips['dgms'][1])

P = set(Point(i[0], i[1]) for i in rips['dgms'][1])

G = list(greedy(P))
# [print(Point(p.x, p.y)) for p in G]

for i in range(1, n):
    with svg_plus_pdf(M, M, 'greedytorus_25_q_'+str(i)) as canvas:
        for p in G[:i]:
            # Change in coordinates to account for plotter orientation
            Point(p.x*scale, M - p.y*scale, radius=4).draw(canvas)

        for p in P:
            # Change in coordinates to account for plotter orientation
            Point(p.x*scale, M - p.y*scale).draw(canvas)

        Line((0, M), (M, 0)).draw(canvas)
