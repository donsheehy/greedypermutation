```python {cmd id="setup"}
from random import randrange, seed
from greedypermutation import GreedyTree
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Line, Group
from greedypermutation.vizpoint import VizPoint as Point
from greedypermutation.vizgreedytree import VizGreedyTree


W = 600
H = 200
N = 100

seed(0)
P = {Point(randrange(5, W//2), randrange(5,H-5)) for i in range(N)} | \
    {Point(randrange(W//2, W-5), randrange(5,H-5)) for i in range(5 * N)}

T = GreedyTree(P)
```

```python {cmd continue="setup" output=html}
# P = {Point(randrange(5, W-5), randrange(5,H-5)) for i in range(150)}
#
# T = GreedyTree(P)

q = Point(478, 92, 3)
nn = Point(*T.nn(q), 3)
r = q.dist(nn)
nn_circle = Point(*q, r)
VT = VizGreedyTree(T)

radius = 61
slack = 0
R = list(T._range(q, radius, slack))
assert(all(q.dist(x.point)<= radius + slack for x in R))
print(T.rangecount(q, radius, slack))


with svg_plus_pdf(W, H, 'greedytree01') as canvas:
    Point(*q, radius).draw(canvas)
    nn_circle.draw(canvas)
    VT.draw(canvas)
    [Point(*x.point, 4).draw(canvas) for x in R]
    q.draw(canvas)
    nn.draw(canvas)
```
