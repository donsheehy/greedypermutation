# Sketches of Persistence Diagrams

```python {cmd id="setup" hide}
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
n = {1,2,3,4,5,10}
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

G = list(greedy(M=D, nbrconstant=2, seed=Point(M//2,M//2), tree=True))
```

This example illustrates how greedy permutations can be used to compute sketches of persistence diagrams.

Consider a sample persistence diagram, $D$, with $50$ points shown below,

```python {cmd continue="setup" output="html" hide}
with svg_plus_pdf(M, M, 'pointset') as canvas:
    [Point(p.x, M-p.y).draw(canvas) for p in points]
    Line((0,M), (M,0)).draw(canvas)
    Line((0,0), (M,0)).draw(canvas)
    Line((M,0), (M,M)).draw(canvas)
    Line((M,M), (0,M)).draw(canvas)
    Line((0,M), (0,0)).draw(canvas)
```

Computing the greedy permutation on these points gives us a collection of greedy sketches of $D$. The entire diagonal is treated as a single point. Sketch $D_i$ contains the first $i$ points of the greedy permutation of points of $D$.

```python {cmd continue="setup"}
G = list(greedy(D))
```

Sketches $D_i$, where $i \in \{1,2,3,4,5,10\}$, are shown below. $D_1$ always contains a single point, the diagonal, with a multiplicity of $50$. Points that are further away are added gradually. The multiplicity of an added and this gives an intuition why a sketch could be considered a good approximation of a persistence diagram at a particular scale.

```python {cmd continue="setup" output="html" hide}
for i in n:
    print("D_"+str(i))
    with svg_plus_pdf(M, M, 'greedysketch_'+str(i)) as canvas:
        for p in G[:i]:
            Point(p[0].x, M - p[0].y, 4).draw(canvas)

        for p in D:
            Point(p.x, M - p.y).draw(canvas)

        Line((0,M), (M,0)).draw(canvas)
        Line((0,0), (M,0)).draw(canvas)
        Line((M,0), (M,M)).draw(canvas)
        Line((M,M), (0,M)).draw(canvas)
        Line((0,M), (0,0)).draw(canvas)
    print('\n')
```