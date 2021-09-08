from metricspaces import MetricSpace
from greedypermutation.clarksongreedy import greedy
from random import randrange, seed
from ds2viz.element import Circle, Line
from ds2viz.canvas import svg_plus_pdf

class Point(Circle):
    def __init__(self, x, y, radius = 1):
        super().__init__(radius)
        self.x, self.y = x, y
        self.align('center', (x,y))

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        return list(self) == list(other)

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return "("+str(self.x)+", "+str(self.y)+")"
    
    def __str__(self) -> str:
        return "("+str(self.x)+", "+str(self.y)+")"

def proj(p: Point):
    return Point((p.x+p.y)/2, (p.x+p.y)/2)

def l_inf(p: Point, q: Point):
    return max(abs(p.x - q.x), abs(p.y - q.y))

def dist(p: Point, q: Point):
    return min(l_inf(p,q), l_inf(p, proj(p))+l_inf(q, proj(q)))

M = 285
N = 50
n = range(1,15)
seed(0)

# Create a random set of points without any duplicates and only 1 point on the diagonal, (M//2,M//2)
points = []
for i in range(N):
    x = randrange(5, M-5)
    points.append(Point(x, randrange(x,M-5)))
points = [i for i in points if i.x != i.y]
points.append(Point(M//2,M//2))
points = list(dict.fromkeys(points))

D = MetricSpace(points = points, dist = dist)

G = list(greedy(M=D, seed=Point(M//2,M//2), tree=True, nbrconstant=2))

print(G[:15])

print("Point \t\t\t Parent \t\t Distance")
for i in n:
    print(str(G[i][0]) + "\t\t" + str(G[G[i][1]][0]) + "\t\t" + str(D.dist(G[i][0], G[G[i][1]][0])))

# print(G)
for i in n:
    with svg_plus_pdf(M, M, 'output/greedysketch_'+str(i)) as canvas:
        for p in G[:i]:
            Point(p[0].x, M - p[0].y, 4).draw(canvas)

        for p in D:
            Point(p.x, M - p.y).draw(canvas)

        Line((0,M), (M,0)).draw(canvas)
        Line((0,0), (M,0)).draw(canvas)
        Line((M,0), (M,M)).draw(canvas)
        Line((M,M), (0,M)).draw(canvas)
        Line((0,M), (0,0)).draw(canvas)