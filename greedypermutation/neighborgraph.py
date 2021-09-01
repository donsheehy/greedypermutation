from ds2.graph import Graph
from greedypermutation.maxheap import MaxHeap


class Cell:
    def __init__(self, center):
        """
        Create a new cell with the given `center`.

        A new cell only contains a single point, its center.
        """
        self.points = {center}
        self.center = center
        self.radius = 0

    def addpoint(self, p):
        """
        Add the point `p` to the cell.
        """
        self.points.add(p)
        self.radius = max(self.radius, self.dist(p))

    def dist(self, point):
        """
        Return the distance between the center of the cell and `point`.
        Note, this allows the cell to be treated almost like a point.
        """
        return self.center.dist(point)

    def updateradius(self):
        """
        Set the radius of the cell to be the farthest distance from a point
        to the center.
        """
        self.radius = max((self.dist(p) for p in self.points), default = 0)

    def pop(self):
        """
        Remove and return the farthest point in the cell.

        Returns `None` if there there are no points other than the center.
        """
        if len(self) == 1:
            return None
        p = max(self.points, key = self.dist)
        # This is linear time!  We should maybe use a heap here.
        # However, the pop is followed by an update that will iterate over all
        # the points anyway.
        # For knn sampling, the pop might not require such an iteration.
        self.points.remove(p)
        self.updateradius()
        return p

    def __len__(self):
        """
        Return the total number of points in the cell, including the center.
        """
        return len(self.points)

    def __iter__(self):
        """
        Return an iterator over the points in the cell.
        """
        return iter(self.points)

    def __contains__(self, point):
        """
        Return True if and only if `point` is in the cell.
        """
        return point in self.points

    def __lt__(self, other):
        """
        Cells are ordered by their radii.
        """
        return self.radius > other.radius

    def __repr__(self):
        return str(self.center)

class NeighborGraph(Graph):
    Vertex = Cell

    # Initialize it as an empty graph.
    def __init__(self, points, root = None, nbrconstant = 1, moveconstant = 1):
        """
        Initialize a new NeighborGraph.

        It starts with an iterable of points.  The first point will be the
        center of the default cell and all other points will be placed
        inside.

        There are two constants that can be set.
        The first `nbrconstant`, which controls the distance between neighbors.
        The second is `moveconstant` which determines when a point is moved
        when a new cell is formed.  The default value for both constants is
        `1`.  This moves a point whenever it has a new nearest neighbor

        The theoretical guarantees are only valid when
        `moveconstant <= nbrconstant`.  As a result, setting these any other
        way raises an exception.
        """
        # Initialize the `NeighborGraph` to be a `Graph`.
        super().__init__()
        P = iter(points)

        if nbrconstant < moveconstant:
            raise RuntimeError("The move constant must not be larger than the"
                               "neighbor constant.")
        self.nbrconstant = nbrconstant
        self.moveconstant = moveconstant
        # Make a cell to start the graph.  Use the first point as the root
        # if none is give.
        root_cell = self.Vertex(root or next(P))
        # Add the points to the root cell.
        # It doesn't matter if the root point is also in the list of points.
        # It will not be added twice.
        for p in P:
            root_cell.addpoint(p)
        # Add the new cell as the one vertex of the graph.
        self.addvertex(root_cell)
        self.addedge(root_cell, root_cell)
        self.heap = MaxHeap([root_cell], key = lambda c: c.radius)

    def iscloseenoughto(self, p, q):
        return q.dist(p.center) <= p.radius + q.radius + \
                      self.nbrconstant * max(p.radius, q.radius)

    def addcell(self, newcenter, parent):
        """
        Add a new cell centered at `newcenter`.

        The `parent` is a suffciently close cell that is already in the
        graph.
        It is used to find nearby cells to be the neighbors.
        The cells are rebalanced with points moving from nearby cells into
        the new cell if it is closer.
        """
        # Create the new cell.
        newcell = self.Vertex(newcenter)
        # Make the cell a new vertex.
        self.addvertex(newcell)
        self.addedge(newcell, newcell)

        # Rebalance the new cell.
        for nbr in self.nbrs(parent):
            self.rebalance(newcell, nbr)
            self.heap.changepriority(nbr)

        # Add neighbors to the new cell.
        for newnbr in self.nbrs_of_nbrs(parent):
            if self.iscloseenoughto(newcell, newnbr):
                self.addedge(newcell, newnbr)

        # After all the radii are updated, prune edges that are too long.
        for nbr in set(self.nbrs(parent)):
            self.prunenbrs(nbr)

        self.heap.insert(newcell)
        return newcell

    def pop(self):
        cell = self.heap.findmax()
        point = cell.pop
        self.heap.changepriority(cell)
        return point

    def rebalance(self, a, b):
        """
        Move points from the cell `b` to the cell `a` if they are
        sufficiently closer to `a.center`.
        """
        points_to_move = {p for p in b.points
                            if a.dist(p) < self.moveconstant * b.dist(p)}
        b.points -= points_to_move
        for p in points_to_move:
            a.addpoint(p)
        # The radius of self (`a`) is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        b.updateradius()

    def nbrs_of_nbrs(self, u):
        return {b for a in self.nbrs(u) for b in self.nbrs(a)}

    def prunenbrs(self, u):
        """
        Eliminate neighbors that are too far with respect to the current
        radius.
        """
        nbrs_to_delete = set()
        for v in self.nbrs(u):
            if not self.iscloseenoughto(u,v):
                nbrs_to_delete.add(v)

        # Prune the excess edges.
        for v in nbrs_to_delete:
            self.removeedge(u,v)
