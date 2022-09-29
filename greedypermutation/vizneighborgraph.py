from ds2viz.styles import *
from ds2viz.default_styles import default_styles
from ds2viz.element import Element
from greedypermutation.convexhull import convexhull

class VizNeighborGraph(Element):

  def __init__(self, neighbor_graph, style='neighborgraph', stylesheet=default_styles):
    super().__init__()
    self.N = neighbor_graph
    self.stylesheet = stylesheet
    self.style = next(self.stylesheet[style])
    
  def draw(self, canvas):
    self.points(canvas)
    self.vertices(canvas)
    self.edges(canvas)
    self.hull(canvas)
    self.label(canvas)

  def points(self, canvas):
    point_style = self.style.get('graph_point')
    if point_style is not None:
      for vertex in self.N.vertices():
        canvas.circle(vertex.center, 2, point_style)
      for cell in self.N.vertices():
        for point in cell.points:
          canvas.circle(point, 2,  point_style)

  def vertices(self, canvas):
    vertex_style = self.style.get('graph_vertex')
    if vertex_style is not None:
      for cell in self.N.vertices():
        for point in cell.points:
          canvas.line(point, cell.center, vertex_style)

  def edges(self, canvas):
    edge_style = self.style.get('cell_edge')
    if edge_style is not None:
      for e in self.N.edges():
          if len(e) == 2:
            u,v = e
            canvas.line(u.center, v.center,  edge_style)
          
  def hull(self, canvas):
    hull_style = self.style.get('convex_hull')
    if hull_style is not None:
      for v in self.N.vertices():
        canvas.polygon(convexhull(v.points), hull_style)

  def label(self, canvas):
    label_style = self.style.get('label')
    if label_style is not None:
      for v in self.N.vertices():
        viz_points = v.points
        for x,y in viz_points.__iter__():
          canvas.text("("+str(x)+","+str(y)+")", (x,y),  label_style)

