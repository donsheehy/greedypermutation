```python {cmd id="point"}
from ds2viz.element import Circle

class Point(Circle):
    def __init__(self, x, y, radius = 1):
        super().__init__(radius)
        self.x, self.y = x, y
        self.align('center', (x,y))

    def __iter__(self):
        yield self.x
        yield self.y

    def dist(self, other):
        return sum((a-b) ** 2 for a,b in zip(self, other)) ** (0.5)

    def __eq__(self, other):
        return list(self) == list(other)

    def __hash__(self):
        return hash((self.x, self.y))
```


```python {cmd id="setup" continue="point"}
from random import randrange, seed
from ds2viz.canvas import svg_plus_pdf
from greedypermutation.knnsample import knnsample
from greedypermutation.clarksongreedy import greedy

W = 600
H = 200
N = 100

seed(0)
P = {Point(randrange(5, W//2), randrange(5,H-5)) for i in range(N)} | \
    {Point(randrange(W//2, W-5), randrange(5,H-5)) for i in range(5 * N)}

G = list(greedy(P))

M = {Point(p.x, p.y, 4) for p in knnsample(P, 25)}
```

## Greedy Sampling

```python {cmd continue="setup" output=html}
with svg_plus_pdf(W, H, 'greedyexample01') as canvas:
    for p in G[:30]:
      Point(p.x, p.y, 4).draw(canvas)

    for p in P:
        p.draw(canvas)
```


## kNN Sampling

```python {cmd continue="setup" output=html}
with svg_plus_pdf(W, H, 'knnexample01') as canvas:
    for p in M:
      p.draw(canvas)

    for p in P:
        p.draw(canvas)
```

Here's a random sample of the same size.
```python {cmd continue="setup" output=html}
P_for_sampling = list(P)
n = len(P)

R = set()
while len(R) < len(M):
    R.add(P_for_sampling[randrange(n)])

with svg_plus_pdf(W, H, 'randomexample01') as canvas:
    for p in {Point(r.x, r.y, 4) for r in R}:
      p.draw(canvas)

    for p in P:
        p.draw(canvas)
```
