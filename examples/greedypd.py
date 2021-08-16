from random import randrange, seed
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Boxed, Line
from greedypermutation.clarksongreedy import greedy
from greedypermutation.vizpoint import VizPoint as Point

M = 300
N = 8
s = 97
n = 2

seed(s)

P = set()
for i in range(N):
    x = randrange(5, M-5)
    P.add(Point(x, randrange(x, M-5)))

G = list(greedy(P))

for i in range(1, n):
    with svg_plus_pdf(M, M, 'greedypd_50_q_'+str(i)) as canvas:
        #r = G[i][1]
        for p in G[:i]:
            # Change in coordinates to account for plotter orientation
            Point(p.x, M - p.y, radius=4).draw(canvas)
            #Boxed(Point(p[0].x, M - p[0].y)).draw(canvas)

        for p in P:
            # Change in coordinates to account for plotter orientation
            Point(p.x, M - p.y).draw(canvas)

        Line((0, M), (M, 0)).draw(canvas)
