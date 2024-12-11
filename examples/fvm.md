# The Finite Voronoi Method

```python{cmd, id=import, hide}
from greedypermutation.fvm.fvmneighborgraph import GreedyFVMNeighborGraph
from greedypermutation.fvm.vizfvmneighborgraph import VizFVMNeighborGraph
from greedypermutation.fvm.utils import TreeParameters
from metricspaces import MetricSpace
from random import randrange, seed
from ds2viz.geometry import VizPoint as Point
from ds2viz.styles import *
from ds2viz.canvas import Canvas
from greedypermutation.fvm.merge import build_tree

seed(1)
ss = StyleSheet.fromyaml("neighbor_graph_style.yaml")

def randompoint(xx, yy):
    return Point(randrange(*xx), randrange(*yy))
```

Here, we run Clarkson's algorithm on two greedy trees and produce a greedy tree with better parameters than the two input trees.

## The Setup
```python{cmd, continue=import, id=setup, output=html}
# Canvas dimension (W x H)
W = 750
H = 450

# Number of points.
N = 1000

# Number of cells
num_cells = 10

P = MetricSpace({randompoint((50, W - 50), (50, H - 50)) for i in range(N)})
```
## Building the Trees
As a toy example, we build trees with different parameters on the two halves of `P`.

```python{cmd, continue=setup, output=html, id=tree}
params_a = TreeParameters(1.04, 1.07, 1.01, 1)
params_b = TreeParameters(1.05, 1.1, 1.01, 1)

tree_a = build_tree(P[:N//2], params_a)
tree_b = build_tree(P[N//2:], params_b)
```

## Building the Finite Voronoi Diagram
Finally, we run the Finite Voronoi Method on both greedy trees as input.
An intermediate FVD is shown below.
The diagram has 11 cells after 10 iterations.
Point location is done on greedy tree nodes using tidy cells.

```python{cmd, continue=tree, output=html}
params = TreeParameters(1.03, 1.05, 1.01, 1)
neighbor_graph = GreedyFVMNeighborGraph([tree_a, tree_b], params)

for i in range(num_cells):
    cell = neighbor_graph.heap.findmax()
    point = cell.farthest.center
    neighbor_graph.addcell(point, cell)

canvas = Canvas(W, H, ss)
ng = VizFVMNeighborGraph(neighbor_graph, "fvm_neighbor_graph", ss)
ng.draw(canvas)
print(canvas.svgout())
```