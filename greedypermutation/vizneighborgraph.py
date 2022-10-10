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
from ds2viz.geometry.convexhull import convexhull

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

    self.__points()
    self.__vertices()
    self.__edges()
    self.__hull()

  def __points(self):
    """
    A private method used to draw points to the canvas if the 'graph_point'
    entry is specified in the stylesheet attribute.
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

  def __vertices(self):
    """
    A private method used to draw lines between the center of a NeighborGraph cell
    and each vertex in contained in the cell of the NeighborGraph to the canvas if 
    the 'graph_vertex' entry is specified in the stylesheet attribute.
    """
    vertex_style = self.style.get('graph_vertex')
    if vertex_style is not None:
      for cell in self.N.vertices():
        for point in cell.points:
          self.addelement(Line(point, cell.center, 'graph_vertex', self.stylesheet))
          #canvas.line(point, cell.center, vertex_style)

  def __edges(self):
    """
    A private method used to draw edges between NeighborGraph cells if the 'graph_edge'
    entry is specified in the stylesheet attribute.
    """
    edge_style = self.style.get('cell_edge')
    if edge_style is not None:
      for e in self.N.edges():
          if len(e) == 2:
            u,v = e
            self.addelement(Line(u.center, v.center, 'cell_edge', self.stylesheet))
          
  def __hull(self):
    """
    A private method used to draw the convex hull around each edge of the 
    NeighborGraph cells if the 'convex_hull' entry is specified in the stylesheet attribute.
    """
    # !!! Interesting behavior with the style lookup.  The group super class does not
    # do a lookup on the stylesheet to ensure the style exists.  So doing the stylecheck
    # in this class is the only way to ensure the style exists in order to render each element.
    hull_style = self.style.get('convex_hull')
    if hull_style is not None:
      for v in self.N.vertices():
        hull_points = convexhull(v.points)
        for i in range(len(hull_points)):
          self.addelement(Line(hull_points[i-1], hull_points[i], 'convex_hull', self.stylesheet))