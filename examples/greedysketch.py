from collections import defaultdict
from os import terminal_size
from metricspaces import MetricSpace
from greedypermutation.clarksongreedy import greedy
from greedypermutation.vizpoint import VizPoint as Point
from random import randrange, seed
from ds2viz.element import Circle, Line
from ds2viz.canvas import svg_plus_pdf

def proj(p: Point):
    return Point((p.x+p.y)/2, (p.x+p.y)/2)

def l_inf(p: Point, q: Point):
    return max(abs(p.x - q.x), abs(p.y - q.y))

def dist(p: Point, q: Point):
    return min(l_inf(p,q), l_inf(p, proj(p))+l_inf(q, proj(q)))

M = 300
N = 50
n = {1,2,3,4,10,20}
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

G = list(greedy(M=D, nbrconstant=2, seed=Point(M//2,M//2), tree=True, gettransportplan=True))

transportplan = defaultdict(int)
#transportplan[Point(M//2,M//2)] = N
    
#print(G[:15])

# print("Point \t\t\t Parent \t\t Distance")
# for i in range(1,11):
#     print(str(G[i][0].x) + "\t\t" + str(G[G[i][1]][0].x) + "\t\t" + str(D.dist(G[i][0], G[G[i][1]][0])))

# print(G)
for i in range(N):
    for m in G[i][2]:
        transportplan[m] += G[i][2][m]

for i in n:
    with svg_plus_pdf(M, M, 'output/greedysketch_'+str(i)) as canvas:
        for p in G[:i]:
            # print(p)
            Point(p[0].x, M - p[0].y, 4).draw(canvas)

        # for m in G[i][2]:
        #     transportplan[m] += G[i][2][m]

        for m in transportplan:
            print("Mass of point ["+str(m.x)+", "+str(m.y)+"]: "+str(transportplan[m]))
        print("end of plan")

        for p in D:
            Point(p.x, M - p.y).draw(canvas)

        Line((0,M), (M,0)).draw(canvas)
        Line((0,0), (M,0)).draw(canvas)
        Line((M,0), (M,M)).draw(canvas)
        Line((M,M), (0,M)).draw(canvas)
        Line((0,M), (0,0)).draw(canvas)