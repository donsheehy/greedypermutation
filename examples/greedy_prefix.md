```python {cmd output="html"}
from ds2viz.element import *
from ds2viz.styles import *
from random import randrange
from metricspaces import MetricSpace
from ds2viz.canvas import Canvas
from greedypermutation.clarksongreedy import greedy
from ds2viz.geometry import VizPoint as Point

ss = StyleSheet.fromstring(
"""
greedy_prefix:
  arrow: null
  point: 'point'
  cover_ball_outline: 'cover_ball_outline'
  cover_ball: 'cover_ball'

arrow:
  stroke_width: 4
  stroke: [1, 0, 0]

point:
  radius: 2
  fill: [0,0,0]
  stroke: [0,0,0]
  stroke_width: 1

prefix_point:
  radius: 8
  fill: [0,0,0]
  stroke: [1,0,0]
  stroke_width: 1

cover_ball_outline:
  stroke: [0,0,0]
  stroke_width: 5

cover_ball:
  stroke_width: 0
  fill: [0.7, 0.7, 1]
""")

class VizGreedyPrefix(Group):
    def __init__(self, GT, k, style='greedy_prefix', stylesheet=default_styles):

        super().__init__()
        style = next(stylesheet[style])
        arrow_style = style['arrow']
        point_style = next(stylesheet[style['point']])
        point_radius = point_style['radius']
        P = list(GT)
        p_k, pred = P[k]
        q_k = P[pred][0]
        r = p_k.dist(q_k)

        for point, _ in P[:k]:
            C = Circle(r, None, 'cover_ball_outline', self.stylesheet)
            C.align('center', point)
            self.addelement(C)
        for point, _ in P[:k]:
            C = Circle(r, None, 'cover_ball', self.stylesheet)
            C.align('center', point)
            self.addelement(C)
        if arrow_style is not None:
            self.addelement(Line(p_k, q_k, 'arrow'))
        for point, _ in P:
            C = Circle(point_radius, None, 'point', self.stylesheet)
            C.align('center', point)
            self.addelement(C)
        for point, _ in P[:k]:
            C = Circle(5, None, 'prefix_point', self.stylesheet)
            C.align('center', point)
            self.addelement(C)

W, H = 1280, 720

def randpt():
    margin = 100
    return Point(randrange(margin, W-margin), randrange(margin, H-margin))

n = 100
samples = 50
P = MetricSpace({randpt() for _ in range(n)})
G = list(greedy(P, tree=True))
gp = VizGreedyPrefix(G, samples, 'greedy_prefix', ss)

canvas = Canvas(W,H,ss)
gp.draw(canvas)
print(canvas.svgout())
```
