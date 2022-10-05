"""Neighbor Graph Visualizer

This module is used as a NeighborGraph utility to draw visualizations of a 
neighbor graph data structure to an SVG canvas.

This module accepts a NeighborGraph object as well as a stylesheet and style attribute.

This script requires 'ds2viz' to be installed within the python environment.

This file contains the following function:
  * draw(canvas) which draws a visualization of a NeighborGraph as an SVG to the parameterized canvas.
"""

from ds2viz.styles import *
from ds2viz.default_styles import default_styles
from ds2viz.element import Element
from greedypermutation.convexhull import convexhull

class VizNeighborGraph(Element):

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
  
  Methods
  -------
  draw(canvas)
    Calls each element function of the VizNeighborGraph to draw individual components of
    the VizNeighborGraph.
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
    
  def draw(self, canvas):
    """
    Delegates drawing to each elements drawing function.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw the VizNeighborGraph too.
    """
    self.__points(canvas)
    self.__vertices(canvas)
    self.__edges(canvas)
    self.__hull(canvas)
    self.__label(canvas)


  def __points(self, canvas):
    """
    A private method used to draw points to the canvas if the 'graph_point'
    entry is specified in the stylesheet attribute.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw this element of VizNeighborGraph too.
    """
    point_style = self.style.get('graph_point')
    if point_style is not None:
      for vertex in self.N.vertices():
        canvas.circle(vertex.center, 2, point_style)
      for cell in self.N.vertices():
        for point in cell.points:
          canvas.circle(point, 2,  point_style)

  def __vertices(self, canvas):
    """
    A private method used to draw lines between the center of a NeighborGraph cell
    and each vertex in contained in the cell of the NeighborGraph to the canvas if 
    the 'graph_vertex' entry is specified in the stylesheet attribute.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw this element of VizNeighborGraph too.
    """
    vertex_style = self.style.get('graph_vertex')
    if vertex_style is not None:
      for cell in self.N.vertices():
        for point in cell.points:
          canvas.line(point, cell.center, vertex_style)

  def __edges(self, canvas):
    """
    A private method used to draw edges between NeighborGraph cells if the 'graph_edge'
    entry is specified in the stylesheet attribute.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw this element of VizNeighborGraph too.
    """
    edge_style = self.style.get('cell_edge')
    if edge_style is not None:
      for e in self.N.edges():
          if len(e) == 2:
            u,v = e
            canvas.line(u.center, v.center,  edge_style)
          
  def __hull(self, canvas):
    """
    A private method used to draw the convex hull around each edge of the 
    NeighborGraph cells if the 'convex_hull' entry is specified in the stylesheet attribute.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw this element of VizNeighborGraph too.
    """
    hull_style = self.style.get('convex_hull')
    if hull_style is not None:
      for v in self.N.vertices():
        canvas.polygon(convexhull(v.points), hull_style)

  def __label(self, canvas):
    """
    A private method used to draw labels as (x,y) coordinates 
    with each point of the NeighborGraph if the 'label' entry 
    is specified in the stylesheet attribute.

    Parameters
    ----------
    canvas: Canvas
      The canvas object to draw this element of VizNeighborGraph too.
    """
    label_style = self.style.get('label')
    if label_style is not None:
      for v in self.N.vertices():
        viz_points = v.points
        for x,y in viz_points.__iter__():
          canvas.text("("+str(x)+","+str(y)+")", (x,y),  label_style)

