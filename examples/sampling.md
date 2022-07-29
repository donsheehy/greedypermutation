# Sampling Euclidean Point Sets

```python {cmd id="setup" hide}
from random import randrange, seed
from greedypermutation import GreedyTree
from metricspaces import MetricSpace
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Line, Group
from greedypermutation.vizpoint import VizPoint as Point
from greedypermutation.vizgreedytree import VizGreedyTree

W = 800
H = 400
N = 300
margin = 40
seed(0)
P = MetricSpace({Point(randrange(margin, W//2), randrange(margin,H-margin)) for i in range(N)} | \
    {Point(randrange(W//2, W-margin), randrange(margin,H-margin)) for i in range(5 * N)})

T = GreedyTree(P)
```

```python {cmd continue}
import numpy as np
from greedypermutation.numpygreedy import sample

delta = margin
A = np.array([list(p) for p in P])

Q = sample(A, delta**2)
```


```python {cmd continue output=html hide}
with svg_plus_pdf(W, H, 'points') as canvas:
    [Point(*Point(*q), delta).draw(canvas) for q in Q]
    [Point(*Point(*q), 3).draw(canvas) for q in Q]
    [Point(*p).draw(canvas) for p in P]
```
