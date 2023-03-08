"""Neighbor Graph Visualizer

This module is used as a NeighborGraph utility to draw visualizations of a 
neighbor graph data structure to an SVG canvas.

This module accepts a NeighborGraph object as well as a stylesheet and style attribute.

This script requires 'ds2viz' to be installed within the python environment.

This classes rendering functionality is delegated to the super class Group and associated
draw methods.
"""

from ds2viz.styles import *
from ds2viz.default_styles import default_styles
from ds2viz.element import *
from ds2viz.geometry import convexhull

class VizNeighborGraph(Group):

  """
  A utility class used to draw visualizations of NeighborGraph objects as 
  a series of points, edges, as well as convex hulls.

  Attributes
  ----------
  neighbor_graph: NeighborGraph
    a NeighborGraph object to draw to a canvas.
  style: str
    The object style used to draw a NeighborGraph as an str. (default 'neighbor_graph')
  stylesheet: StyleSheet
    The stylesheet used to describe which elements to draw an how to draw them. (default ds2viz.default_styles)
  """
  
  def __init__(self, neighbor_graph, style='neighbor_graph', stylesheet=default_styles):
    """
    Parameters
    ----------
    neighbor_graph: NeighborGraph
      a NeighborGraph object to draw to a canvas.
    style: str, optional
      The object style used to draw a NeighborGraph as an str. (default 'neighbor_graph')
    stylesheet: StyleSheet, optional
      The stylesheet used to describe which elements to draw an how to draw them.
      This parameter accepts a StyleSheet object not a YAML file.  (default ds2viz.default_styles)
    """

    super().__init__()
    self.N = neighbor_graph
    self.stylesheet = stylesheet
    self.style = next(self.stylesheet[style])
    
    self._vertices()
    self._edges()
    self._hull()
    self._points()

  def _points(self):
    """
    A private method used to add points to the neighbor graph group.
    """
    point_style = self.style.get('graph_point')
    if point_style is not None:
      for vertex in self.N.vertices():
        C = Circle(2, None, 'graph_point', self.stylesheet)
        C.align('center', vertex.center)
        self.addelement(C)
        # canvas.circle(vertex.center, 2, point_style)
      for cell in self.N.vertices():
        for point in cell.points:
          C = Circle(2, None, 'graph_point', self.stylesheet)
          C.align('center', point)
          self.addelement(C)
          # canvas.circle(point, 2,  point_style)

  def _vertices(self):
    """
    A private method used to lines between the graph vertex and 
    the contained points to the neighbor graph group.
    """
    vertex_style = self.style.get('graph_vertex')
    if vertex_style is not None:
      for cell in self.N.vertices():
        for point in cell.points:
          self.addelement(Line(point, cell.center, 'graph_vertex', self.stylesheet))
          #canvas.line(point, cell.center, vertex_style)

  def _edges(self):
    """
    A private method used to add edges between graph vertices to the neighbor graph group.
    """
    edge_style = self.style.get('cell_edge')
    if edge_style is not None:
      for e in self.N.edges():
          if len(e) == 2:
            u,v = e
            self.addelement(Line(u.center, v.center, 'cell_edge', self.stylesheet))
          
  def _hull(self):
    """
    A private method used to add a convex hull to the neighbor graph group.
    """
    hull_style = self.style.get('convex_hull')
    if hull_style is not None:
      for v in self.N.vertices():
        self.addelement(Polygon(convexhull(v.points), 'convex_hull', self.stylesheet))
        # hull_points = convexhull(v.points)
        # for i in range(len(hull_points)):
        #   self.addelement(Line(hull_points[i-1], hull_points[i], 'convex_hull', self.stylesheet))