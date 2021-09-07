from metricspaces import MetricSpace
# from metricspaces import QuotientSpace
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

M = 240
N = 50
n = {1,2,3,4,5,10}
seed(0)

# Create a random set of points without any duplicates and only 1 point on the diagonal, (0,0)
points = []
for i in range(N):
    x = randrange(5, M-5)
    points.append(Point(x, randrange(x,M-5)))
points = [i for i in points if i.x != i.y]
points.append(Point(0,0))
points = list(dict.fromkeys(points))
# print(len(points))
# print(points[:5])

# X = MetricSpace(points = points, dist=l_inf)

X_Y = MetricSpace(points = points, dist = dist)

G = list(greedy(M=X_Y, alpha=1, seed=Point(0,0), tree=True))
print("Point \t\t\t Parent \t\t Distance")
for i in n:
    print(str(G[i][0]) + "\t\t" + str(G[G[i][1]][0]) + "\t\t" + str(X_Y.dist(G[i][0], G[G[i][1]][0])))

# print(G)
for i in n:
    with svg_plus_pdf(M, M, 'output/greedysketch_'+str(i)) as canvas:
        for p in G[:i]:
            Point(p[0].x, M - p[0].y, 4).draw(canvas)

        for p in X_Y:
            Point(p.x, M - p.y).draw(canvas)

        Line((0,M), (M,0)).draw(canvas)