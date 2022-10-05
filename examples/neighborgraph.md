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
from greedypermutation.vizpoint import VizPoint as Point

# Canvas dimension (W x H)
W = 500
H = 300

# Number of points.
N = 500
num_cells = 12

# Import the example stylesheet.
ss = StyleSheet.fromyaml('neighbor_graph_style.yaml')

# Initialize metric space.
metric_space = MetricSpace({Point(randrange(W), randrange(H)) for i in range(N)})

# Construct a neighbor graph and iteratively add points to the neighbor graph.
neighbor_graph = GreedyNeighborGraph(metric_space)
for i in range(num_cells):
  cell = neighbor_graph.heap.findmax()
  point = cell.farthest
  neighbor_graph.addcell(point, cell)

# Initialize the canvas.
canvas = Canvas(W, H, ss)

# Construct a VizNeighborGraph object using the neighbor graph, the stylesheet, and the style on the style sheet
# to designate which elements to draw.
VizNeighborGraph(neighbor_graph, 'neighbor_graph', StyleSheet.fromyaml('neighbor_graph_style.yaml')).draw(canvas)

# Print the canvas as an SVG.
print(canvas.svgout())
```