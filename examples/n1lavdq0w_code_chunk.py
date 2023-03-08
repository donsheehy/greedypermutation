from random import randrange, seed

from metricspaces import MetricSpace
from ds2viz.styles import *
from ds2viz.datastructures import VizBST
from ds2viz.canvas import svg_plus_pdf, Canvas
from ds2viz.geometry import VizPoint as Point
from greedypermutation.balltree import greedy_tree
from greedypermutation.vizgreedytree import VizGreedyTree

# Canvas dimension (W x H)
W = 500
H = 300

# Number of points.
N = 5

ss = StyleSheet.fromstring(
  """
  greedy_tree:
    ball: 'ball'
    left: 'left'
    right: 'right'

  ball:
    stroke: [0,0,0]
    stroke_width: 1
    fill: [1,1,1]

  left:
    stroke: [0,1,0]
    stroke_width: 1
  
  right:
    stroke: [1,0,0]
    stroke_width: 1
  """
)
metric_space = MetricSpace({Point(randrange(W*0.15, W*0.85), randrange(H*0.15, H*0.85)) for i in range(N)})

tree = greedy_tree(metric_space)
canvas = Canvas(W, H, ss)

vt = VizGreedyTree(tree, W, H, 'greedy_tree', ss)
vt.draw(canvas)
print(canvas.svgout())
