### VizNeighborGraph
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

W = 500
H = 300
N = 500
num_cells = 12

ss = StyleSheet.fromyaml('neighbor_graph_style.yaml')
# Initialize MetricSpace with a random number for points within the parameterized
# width and height.
metric_space = MetricSpace({Point(randrange(W), randrange(H)) for i in range(N)})
'''
def makemouth(num_steps=100):
  mouth = []
  x_off = 250
  y_off = 150
  r = 145
  
  step = (Math.pi*2)/num_steps
  i = 0
  while i <= num_steps:
    x = r * Math.cos(step*i)
    y = r * Math.sin(step*i)
    mouth.append(Point(x + x_off, y + y_off))
    i = i + 1

  return mouth
metric_space = MetricSpace(makemouth(50))

# Create a NeighborGraph from the MetricSpace
neighbor_graph = GreedyNeighborGraph(metric_space)
vg = VizNeighborGraph(neighbor_graph, 'neighbor_graph', 'neighbor_graph_style')
'''
neighbor_graph = GreedyNeighborGraph(metric_space)
for i in range(num_cells):
  cell = neighbor_graph.heap.findmax()
  point = cell.farthest
  neighbor_graph.addcell(point, cell)
  #canvas = Canvas(W, H, ss)
  #vg.draw(canvas)
  #print(canvas.svgout())

canvas = Canvas(W, H, ss)
VizNeighborGraph(neighbor_graph, 'neighbor_graph', StyleSheet.fromyaml('neighbor_graph_style.yaml')).draw(canvas)
print(canvas.svgout())
```