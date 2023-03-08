### VizGreedyTree
```python {cmd id="setup"}
from random import randrange, seed
from metricspaces import MetricSpace
from ds2viz.styles import *
from ds2viz.datastructures import VizBST
from ds2viz.canvas import svg_plus_pdf, Canvas
from ds2viz.geometry import VizPoint as Point
from greedypermutation.balltree import greedy_tree
from greedypermutation.vizgreedytree import VizGreedyTreeGraph, VizGreedyTreeBST
from greedypermutation.vizneighborgraph import VizNeighborGraph
from greedypermutation.neighborgraph import GreedyNeighborGraph
from ds2viz.datastructures import VizBST
# Canvas dimension (W x H)
W = 1000
H = 1000

# Number of points.
N = 20
num_cells = 10

ss = StyleSheet.fromstring(
  """
  greedy_tree:
    ball: 'ball'
    left: 'left'
    right: 'right'
    construction_node: 'construction_node'
    construction_edge: 'construction_edge'

  construction_node:
    stroke: [0,0,0]
    stroke_width: 3
    fill: [1,1,1]
  
  construction_edge:
    stroke_width: 2
    stroke: [0, 0, 0]

  ball:
    stroke:  [0.7, 0.7, 0.7]
    stroke_width: 3
    fill: null

  left:
    stroke: [0,1,0]
    stroke_width: 1
  
  right:
    stroke: [1,0,0]
    stroke_width: 1

  neighbor_graph:
    graph_point: 'graph_point'

  cell_edge:
    stroke_width: 1
    stroke: [0.7, 0.7, 0.7]

  graph_point:
    radius: 4
    fill: [0,0,0]
    stroke: [0,0,0]
    stroke_width: 1
  """
)

metric_space = MetricSpace({Point(randrange(W*0.15, W*0.85), randrange(W*0.15, W*0.85)) for i in range(N)})


neighbor_graph = GreedyNeighborGraph(metric_space)

for i in range(num_cells):
  cell = neighbor_graph.heap.findmax()
  point = cell.farthest
  neighbor_graph.addcell(point, cell)


tree = greedy_tree(metric_space)
canvas1 = Canvas(W, H, ss)
canvas2 = Canvas(W, H)


vt = VizGreedyTreeGraph(tree, 'greedy_tree', ss)
vtBST = VizGreedyTreeBST(tree)
ng2 = VizNeighborGraph(neighbor_graph, 'neighbor_graph', ss)
vt.draw(canvas1)
ng2.draw(canvas1)
vtBST.draw(canvas2)

print(canvas1.svgout())
print(canvas2.svgout())
```