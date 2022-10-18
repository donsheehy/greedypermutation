```python {cmd id="setup"}
from random import randrange, seed
from ds2viz.canvas import svg_plus_pdf
from ds2viz.element import Circle
from ds2viz.styles import StyleSheet
from greedypermutation.knnsample import knnsample
from greedypermutation.clarksongreedy import greedy
from greedypermutation.onehopgreedy import onehopgreedy
from metricspaces import MetricSpace

ss = StyleSheet.fromyaml('stylesheet.yaml')

class Point(Circle):
    def __init__(self, x, y, style = '_point', radius=None):
        if radius is None:
            radius = next(ss[style])['radius']
        super().__init__(radius, style = style)
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


def _dist(point, S):
    return min(point.dist(s) for s in S)

def _disth(A, B):
    return max(_dist(a, B) for a in A)

def distH(A, B):
    return max(_disth(A,B), _disth(B,A))

W = 300
H = 300
N = 200
k = 25
margin = 20
seed(0)
P = MetricSpace(list({Point(randrange(margin, W-margin), randrange(margin,H-margin)) for i in range(N)}))
n = len(P)

G = list(greedy(P))

M = [Point(p.x, p.y, '_circle') for p in onehopgreedy(P)]

def drawsample(name, P, sample, k, radius):
  radius = distH(P, sample)
  with svg_plus_pdf(W, H, name, ss) as canvas:
      for p in sample:
          Point(p.x, p.y, 'cover_back', radius).draw(canvas)
      for p in sample:
          Point(p.x, p.y, 'cover', radius).draw(canvas)

      for p in P:
          p.draw(canvas)

```

## One Hop Greedy Sampling

```python {cmd continue="setup" output=html}
sample = M[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-01', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)
```

```python {cmd continue="setup" output=html}
sample = G[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-02', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)
```

```python {cmd continue="setup" output=html}
k = 10
sample = M[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-01_10pts', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)

sample = G[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-02_10pts', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)
```

```python {cmd continue="setup" output=html}
k = 50
sample = M[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-01_50pts', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)

sample = G[:k]
radius = distH(P, sample)
drawsample('onehopgreedy-02_50pts', P, sample, k, radius)
print('<br/><hr/>radius = ', radius)
```


```python {cmd continue="setup", matplotlib}
import matplotlib.pyplot as plt
import numpy as np

n = 30
onehopradii = [_dist(M[i], M[:i]) for i in range(1,n)]
greedyradii = [_dist(G[i], G[:i]) for i in range(1,n)]

# evenly sampled time at 200ms intervals
# t = range(1,n-1)

# red dashes, blue squares and green triangles
plt.ylabel('coverage radius')
plt.xlabel('number of points')
plt.plot(onehopradii, label="one hop greedy")
plt.plot(greedyradii, label="pure greedy")
plt.legend()
plt.show()    
```
