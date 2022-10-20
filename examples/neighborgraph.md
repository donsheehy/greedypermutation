### VizNeighborGraph

This example constructs a 12 cell neighbor graph from a metric space 500 points.
Next, the neighbor graph is passed to VizNeighborGraph to draw a representation of the neighbor graph on the canvas.

Point locations in the metric space are determined randomly.

```python {cmd id="setup"}
import math as Math
from random import randrange, seed
from ds2viz.styles import *
from ds2viz.canvas import svg_plus_pdf, Canvas
from ds2viz.element import Element
from metricspaces import MetricSpace
from greedypermutation import Cell, NeighborGraph
from greedypermutation.neighborgraph import GreedyNeighborGraph
from greedypermutation.vizneighborgraph import VizNeighborGraph
from ds2viz.geometry import VizPoint as Point

# Canvas dimension (W x H)
W = 500
H = 300

# Number of points.
N = 500
num_cells = 12

# Import the example stylesheet.
ss1 = StyleSheet.fromyaml('neighbor_graph_style.yaml')

ss2 = StyleSheet.fromstring(
"""
neighbor_graph:
  cell_edge: 'cell_edge'
  graph_point: 'graph_point'

cell_edge:
  stroke_width: 1
  stroke: [0.7, 0.7, 0.7]

graph_point:
  radius: 4
  fill: [0,0,0]
  stroke: [0,0,0]
  stroke_width: 1
""")

# Initialize metric space.
metric_space = MetricSpace({Point(randrange(W), randrange(H)) for i in range(N)})

# Construct a neighbor graph and iteratively add points to the neighbor graph.
neighbor_graph = GreedyNeighborGraph(metric_space)
for i in range(num_cells):
  cell = neighbor_graph.heap.findmax()
  point = cell.farthest
  neighbor_graph.addcell(point, cell)

# Initialize the canvas.
canvas1 = Canvas(W, H, ss1)
canvas2 = Canvas(W, H, ss2)


# Construct a VizNeighborGraph object using the neighbor graph, the stylesheet, and the style on the style sheet
# to designate which elements to draw.
ng1 = VizNeighborGraph(neighbor_graph, 'neighbor_graph', ss1)
ng2 = VizNeighborGraph(neighbor_graph, 'neighbor_graph', ss2)
# ng.align((10, 10))
# Can now align all elements as a group.
ng1.draw(canvas1)
ng2.draw(canvas2)
# Print the canvas as an SVG.
print(canvas1.svgout())
print(canvas2.svgout())
```