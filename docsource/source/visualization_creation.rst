Creating Visualizers
===============
This should serve as a tutorial for creating standardized visualizations for `greedypermutation`.

Current Visualizers
===============
There are currently two visualizers in `greedypermutation`:
1. `VizNeighborGraph`
2. `VizGreedyTree`.  

These two visualizers are used to visualize a `NeighborGraph` and a `BallTree` respectively.  Both visualizers share similar design principles.

Process for Developing Visualizers
===============
A visualizer is used to visualize a data structure.  Each visualizer should act as a wrapper class for the data structure it visualizes.  The visualizer should not construct the data structure or mutate the data structure.  The visualizer should only inspect the contents of the data structure to draw the data structure to the canvas.

A visualizer class should inherit the `Group` class to allow the entire visualized data structure to be aligned independent of the canvas it is drawn on.  Additionally, a visualizer should follow the naming convention of adding the prefix "Viz" to the name of the data structure to be visualized.  For example, the `NeighborGraph` structure is visualized using the `VizNeighborGraph` class.

INITIALIZER 

Each visualizer class should have an initializer with at three parameters
1. A parameter to represent the data structure being visualized.
2. A parameter to represent the style to be used when drawing the data structure.  This parameter should have a default parameter with the name of the visualized data structure.
3. A parameter to represent the style sheet to be used to draw the data structure.  This parameter should have a default value of "default_styles".

Example:
The initializer for `VizNeighborGraph` is `__init__(self, neighbor_graph, style, stylesheet)`, the `neighbor_graph` parameter references the `NeighborGraph` object to be visualized.  The `style` attribute references the style on the parameterized style sheet to be used to draw components of the neighbor graph.  The `stylesheet` attribute references the `.yaml` style sheet to be used to draw the neighbor graph.

The initializer should use these parameters as attributes for the entire class.  Additionally, the initializer needs to call `next(self.stylesheet[style])` (where `style` and `stylesheet` are parameters to the initializer) to get the style to be used from the parameterized style sheet.  This should be saved as a class attribute.  Last, the current convention is for the initializer to call all component (helper) methods to draw components of a visualization to the `Canvas`.

METHODS

Methods in a visualizer represent major components of a data structure.  
For example, a `NeighborGraph` has points in the plane, cells, edges between cells, etc.  Each of these represents a different major component that needs to be drawn to the canvas.  The components are represented by the methods `_points()`, `_vertices()`, `_edges()`, etc.  The initializer should call each of these methods delegating the task of drawing the component to the component method.

Each component method should first validate if the component should be drawn or not.  Listing the style of a component under the primary style tells the visualizer to draw or not to draw a component of the data structure.  The current method to determine wether or not to draw a component is as follows: `validate_style = self.style.get('style_name')` where `style_name` is the name of this component style to look for in the style sheet.  `Validate_style` can then be `None` validated.  If `Validate_style` is `None`, then the component should not be drawn, otherwise, the style exists and the component should be drawn.

The body of a component method should follow this `None` check for the style name.  To add components to the drawing, the component method should call `self.addelement(Element)` where `Element` is the `Element` to add to the `Group`.  This is the only constraint on the body of a component method.

DRAWING

To draw a visualization, the user should construct the data structure to be visualized.  This data structure should then be passed to its corresponding wrapper class along with a style and style sheet that the data structure should be drawn with.  To draw the data structure, the user should call the `draw()` method on the visualization object.

For an example of how this is done, see `greedypermutation\examples\neighborgraph.md``

