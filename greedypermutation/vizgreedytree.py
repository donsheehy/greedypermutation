from ds2viz.element import Group, Line
from ds2viz.element import Circle, Empty
from ds2viz.default_styles import default_styles

class VizGreedyTreeGraph(Group):
    """
    A utility class used to draw visualizations of BallTrees.

    Attributes
    ----------
    greedy_tree: BallTree
        A ball tree to draw to a graph.
    style: str
        The object style used to draw a VizGreedyTree as an str. (default 'greedy_tree')
    stylesheet: StyleSheet
        The stylesheet used to describe which elements to draw an how to draw them. (default ds2viz.default_styles)
    """
    def __init__(self, greedy_tree, style='greedy_tree', stylesheet=default_styles):
        super().__init__()
        self.greedy_tree = greedy_tree
        self.stylesheet = stylesheet
        self.style = next(self.stylesheet[style])
        self._ball_radii(self.greedy_tree)
        self._overlay_tree(self.greedy_tree, self.greedy_tree)

    def _ball_radii(self, root):
        """
        This private method is used to traverse the ball tree and add the radii of each ball to 
        the Group as a circle with a radius equivalent to that of the ball in the tree.

        Parameters
        ----------
        root: BallTreeNode
            The root node of the greedy_tree attribute.
        """
        if root is None:
            return

        C = Circle(root.radius, None, 'ball', self.stylesheet)            
        C.align('center', root.center)
        self.addelement(C)

        self._ball_radii(root.left)
        self._ball_radii(root.right)
    
    def _overlay_tree(self, root, prev):
        """
        This private method is used to overlay a tree onto an image with the location of each node corresponding 
        to the center of each ball.  Each tree consists of circle connected by lines.  The radius of each 
        circle is arbitrary.

        Parameters
        ----------
        root: BallTreeNode
            The root node of the greedy_tree attribute.
        prev: BallTreeNode
            The previous node visited in the traversal to draw a connecting line from.
        """
        if root is None:
            return

        if root == prev:
            R = Circle(10, None, 'construction_node', self.stylesheet)
            R.align('center', root.center)
            self.addelement(R)

        C = Circle(5, None, 'construction_node', self.stylesheet)
        C.align('center', root.center)
        L = Line(prev.center, root.center, 'construction_edge', self.stylesheet)
        self.addelement(L)
        self.addelement(C)

        self._overlay_tree(root.left, root)
        self._overlay_tree(root.right, root)
    

class VizGreedyTreeBST(Group):
    def __init__(self, n, position = (0,0)):
        super().__init__()
        self.position = position
        self.lefttree = VizGreedyTreeBST(n.left) if n.left else Empty()
        self.righttree = VizGreedyTreeBST(n.right) if n.right else Empty()
        self.root = Circle(22, label = str(round(n.radius, 3)))
        self.root.halign('left', self.lefttree.a('right'))
        self.righttree.halign('left', self.root.a('right'))

        for ch in [self.righttree, self.lefttree]:
            ch.valign('top', self.root.a('bottom'))
            
        rootcenter = self.root.a('center')
        self.setanchor('root', rootcenter)

        for child in [self.lefttree, self.righttree]:
            if child:
                self.addelement(Line(rootcenter, child.a('root')))
                self.addelement(child)
        self.addelement(self.root)