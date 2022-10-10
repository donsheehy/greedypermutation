Neighbor Graph Visualizer
===============

`vizneighborgraph.py` is a utility for visualizing Neighbor Graphs utilizing `ds2viz`.  The neighbor graph visualizer is represented as a class, `VizNeighborGraph`.  A `VizNeighborGraph` inherits from `Element` in `ds2viz`  This class has the initializer:

- `__init__(self, neighbor_graph, style, stylesheet)` This initializer accepts a NeighborGraph object from `greedypermutation`, a specified style as a string, and a `.yaml` stylesheet.  The `style` parameter is used to look up the parameterized style in the stylesheet.  Each parameter is set to a new class attribute with the same identifier and value as the parameter.

Additionally, `VizNeighborGraph` has six methods used to draw elements of the `NeighborGraph` object to a `Canvas` object.  To draw elements, call the `super().draw()` method to draw a `VizNeighborGraph`.  Specifying which elements of the `NeighborGraph` are drawn to the canvas is handled by the stylesheet attribute.

- `__points(self)` This method is used to draw the points of the NeighborGraph to the canvas.  To specify drawing points to the canvas, the 'graph_point' name should be used to wrap the style specifications of NeighborGraph points.
- `__vertices(self)` This method is used to draw lines from the center of one `NeighborGraph` cell to the center of cells vertices.  To specify drawing vertices to the canvas, the `graph_vertex` name should be used to wrap the style specifications of `NeighborGraph` vertices.
- `__edges(self)` This method is used to draw the edges of the `NeighborGraph` object to the canvas.  Edges are drawn as the point in the center of a `NeighborGraph` cell.  To specify drawing edges to the canvas, the `graph_edge` name should be used to wrap the style specifications of Neighbor Graph edges.
- `__hull(self)` This method is used to draw a convex hull around a `NeighborGraph` cell.  The convex hull is drawn as a polygon around the outermost points of the `NeighborGraph` cell.  The task of computing the convex hull is delegated to the `ConvexHull` class part of `ds2viz`.  To specify drawing a convex hull to the canvas, the `convex_hull` name should be used to wrap the style specifications of the Neighbor Graph hull.

Visualizer Styles
===============
Currently, a `VizNeighborGraph` draws a `NeighborGraph` as five different components.  These components are the following:

- The points of the neighbor graph.
- The vertices/cells of the neighbor graph.
- The edges from one cell to the next cell of the neighbor graph.
- The convex hull surrounding each cell of the neighbor graph.

Specifying which elements to draw is done on a `.yaml` stylesheet which is then passed to `VizNeighborGraph`.  The format for a `VizNeighborGraph` stylesheet should have the following:

An entry for the style parameter for a `VizNeighborGraph` object.  This will be the object style.  These style names should match or else `VizNeighborGraph` will fail to look up the correct styles to use and will not draw anything.  Inside the entry, there should be 1-5 entries for each element style.  These entries are used to look up the specific element style inside of the object style.  These entries must match the naming conventions below:

1. `graph_point` should specify the style for points on the graph.
2. `graph_vertex` should specify the style for the lines between the cell center an each vertex on the graph.
3. `graph_edge` should specify the style edges between cells on the graph.
4. `convex_hull` should specify the style for the convex hull drawn around a cell on the graph.

To not draw an element, simply do not list the element as an entry in the object style entry.

For an example style sheet for a `VizNeighborGraph` object see `greedypermutation/examples/neighbor_graph_style.yaml`.

For example usage of a `VizNeighborGraph` drawing see `greedypermutation/examples/neighborgraph.md`