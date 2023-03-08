Greedy Tree (Ball Tree) Visualizer
===============

`vizgreedytree.py` is a utility for visualizing greedy trees or ball trees.  The greedy tree visualizer is represented by 2 classes; `VizGreedyTree` and `VizGreedyTreeBST`.  A `VizGreedyTree` and `VizGreedyTreeBST` both inherit from `Group`

`VizGreedyTree`
This class has the constructor:
- `__init__(self, greedy_tree, style='greedy_tree', stylesheet=default_styles)`  This initializer accepts a GreedyTree object from `greedypermutation\balltree`, a specified a specified style as a string, and a `.yaml` stylesheet.  The `style` parameter is used to look up the parameterized style in the stylesheet.  Each parameter is set to a new class attribute with the same identifier and value as the parameter.

Additionally, `VizGreedyTree` has two methods used to draw elements of the `VizGreedyTree` object to a `Canvas` object.  To draw elements, call the `super().draw()` method to draw a `VizGreedyTree`.  Specifying which elements of the `VizGreedyTree` are drawn to the canvas is handled by the stylesheet attribute.

- `_ball_radii(self, root)` This method is used to draw each ball in the tree in the plane.  Each ball is drawn as a `Circle` with its radius specified from the `GreedyTree` object.  Each ball is drawn in pre-order.
- `_overlay_tree(self, root, prev)` This method is used for overlaying a greedy tree graph in the plane.  This method shows a greedy trees construction edges in the plane given a root node.

`VizGreedyTree`
This class has the constructor:
`__init__(self, n, position = (0,0))` This initializer accepts a greedy tree `n` and a position tuple to offset the visualized greedy tree to.  This class is used to show the construction of a ball tree as a binary tree.  Each ball is shown as a node in the binary tree.  The radius of each node is arbitrary.  This class has no other methods.

Visualizer Styles
===============
Currently, a `VizGreedyTree` draws a `GreedyTree` as two different components.  These components are the following:

- The balls in the plane.
- The construction edges between balls.

*** `VizGreedyTreeBST` draws a `GreedyTree` as a single binary tree.

Specifying which elements to draw is done on a `.yaml` stylesheet which is then passed to `VizGreedyTree`.  The format for a `VizGreedyTree` stylesheet should have the following:

An entry for the style parameter for a `VizGreedyTree` object.  This will be the object style.  These style names should match or else `VizGreedyTree` will fail to look up the correct styles to use and will not draw anything.  Inside the entry, there should be 1-5 entries for each element style.  These entries are used to look up the specific element style inside of the object style.  These entries must match the naming conventions below:

1. `construction_node` should specify the style for construction edges in the planar graph.
2. `ball` should specify the style for a ball in the plane.

*** `VizGreedyTreeBST` defaults to the default styles and is currently not mutable.

To not draw an element, simply do not list the element as an entry in the object style entry.

For an example style sheet for a `VizGreedyTree` object see `greedypermutation/examples/greedy_tree.md`. (inline stylesheet)

For example usage of a `VizNeighborGraph` drawing see `greedypermutation/examples/greedy_tree.md`