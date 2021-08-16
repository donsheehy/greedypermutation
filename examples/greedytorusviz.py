from greedypermutation.clarksongreedy import greedy
from cairo import Context, SVGSurface, PDFSurface, ImageSurface, FORMAT_ARGB32
from ds2viz.element import Circle, Line
from ds2viz.canvas import svg_plus_pdf
from random import randrange, seed
from math import pi
from tadasets import torus
from ripser import ripser
import cairo
import math

#from persim import plot_diagrams

POINTS_PER_INCH = 72
INCHES = 20


def _l_inf(p, q):
    return max(abs(p.x-q.x), abs(p.y-q.y))


def _proj(p):
    return Point((p.x + p.y)/2, (p.x+p.y)/2)


class Point(Circle):
    def __init__(self, x, y, radius=1):
        self.x = x
        self.y = y
        self.radius = radius

    def __repr__(self) -> str:
        return("("+str(self.x)+","+str(self.y)+")")

    def dist(self, other):
        return min(_l_inf(self, other), _l_inf(self, _proj(self)) + _l_inf(other, _proj(other)))


def draw_pd(points):
    image = ImageSurface(FORMAT_ARGB32, INCHES*POINTS_PER_INCH,
                         INCHES*POINTS_PER_INCH)
    ctx = Context(image)
    ctx.scale(INCHES*POINTS_PER_INCH,
              INCHES*POINTS_PER_INCH)
    # ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(0.001)
    # ctx.stroke()

    ctx.move_to(0, 0)
    ctx.line_to(INCHES*POINTS_PER_INCH, INCHES*POINTS_PER_INCH)
    # ctx.close_path()
    ctx.stroke()
    for p in points:
        ctx.arc(p[0]*POINTS_PER_INCH, p[1] *
                POINTS_PER_INCH, 1*POINTS_PER_INCH, 0, 2*pi)
        ctx.stroke()
    # pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    # pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
    # pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

    # ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    # ctx.set_source(pat)
    # ctx.fill()

    # ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

    # ctx.move_to(0, 0)
    # # Arc(cx, cy, radius, start_angle, stop_angle)
    # ctx.arc(0.2, 0.1, 0.1, -math.pi / 2, 0)
    # ctx.line_to(0.5, 0.1)  # Line to (x,y)
    # # Curve(x1, y1, x2, y2, x3, y3)
    # ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
    # ctx.close_path()

    # ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
    # ctx.set_line_width(0.02)
    # ctx.stroke()

    # image.write_to_png("example.png")

    image.write_to_png("greedy.png")


seed(0)
M = 300
n = 5

base_set = torus(n=200, c=2, a=1)
rips = ripser(base_set)

# print(rips['dgms'][1])
# plot_diagrams(rips['dgms'][1])

P = set(Point(i[0], i[1]) for i in rips['dgms'][1])

draw_pd(rips['dgms'][1])

G = list(greedy(P))
[print(Point(p.x, p.y)) for p in G]

# for i in range(1, n):
#     with svg_plus_pdf(M, M, 'greedytorus_200_q_'+str(i)) as canvas:
#         #r = G[i][1]
#         for p in G[:i]:
#             # Change in coordinates to account for plotter orientation
#             Point(p.x, M - p.y, radius=4).draw(canvas)

#         for p in P:
#             # Change in coordinates to account for plotter orientation
#             Point(p.x, M - p.y).draw(canvas)

#         Line((0, M), (M, 0)).draw(canvas)
