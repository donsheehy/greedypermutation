from collections import defaultdict
from typing import DefaultDict
from ds2.graph import Graph
from metricspaces import metric_class
from greedypermutation.maxheap import MaxHeap


@metric_class
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
        d = self.dist(p)
        if d > self.radius:
            self.radius = d
            self.farthest = p

    def dist(self, point):
        """
        Return the distance between the center of the cell and `point`.
        Note, this allows the cell to be treated almost like a point.
        """
        return self.metric.dist(self.center, point)

    def comparedist(self, point, other, alpha):
        """
        Return True iff `point` is closer to the center of this cell
        than to the center of the `other` cell. `alpha` is the moveconstant.
        """
        return self.metric.comparedist(point,
                                       self.center,
                                       other.center,
                                       alpha=alpha)

    def updateradius(self):
        """
        Set the radius of the cell to be the farthest distance from a point
        to the center.

        Also, store the farthest point.
        """
        max_dist = 0
        max_point = None
        for p in self.points:
            d = self.dist(p)
            if d > max_dist:
                max_dist = d
                max_point = p
        self.radius = max_dist
        self.farthest = max_point

    def __len__(self):
        """
        Return the total number of points in the cell, including the center.
        """
        # Sid: Might be better to use `NeighborGraph.cellmass(cell)`
        #  to account for multiplicity
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
    def __init__(self,
                 M,
                 root=None,
                 nbrconstant=1,
                 moveconstant=1,
                 gettransportplan=False,
                 mass=None):
        """
        Initialize a new NeighborGraph.

        It starts with an iterable of points of a metric space.
        The first point will be the center of the default cell and all
        other points will be placed inside.

        There are two constants that can be set.
        The first `nbrconstant`, which controls the distance between neighbors.
        The second is `moveconstant` which determines when a point is moved
        when a new cell is formed.  The default value for both constants is
        `1`.  This moves a point whenever it has a new nearest neighbor

        The theoretical guarantees are only valid when
        `moveconstant <= nbrconstant`.  As a result, setting these any other
        way raises an exception.

        `gettransportplan` is a flag that determines whether `addcell()`
        computes transportation plans or not.
        """
        # Initialize the `NeighborGraph` to be a `Graph`.
        super().__init__()
        if mass is None:
            mass = [1]*len(M)
        elif len(mass) != len(M):
            raise ValueError("`mass` must of same length as `M`")
        self.mass = defaultdict(int)
        for i, p in enumerate(M):
            self.mass[p] += mass[i]

        # Establish a class for the cells.
        self.Vertex = Cell(M)

        if nbrconstant < moveconstant:
            raise RuntimeError("The move constant must not be larger than the"
                               "neighbor constant.")
        self.nbrconstant = nbrconstant
        self.moveconstant = moveconstant

        # self.gettransportplan is a flag which determines whether the
        # transportation plan is to be computed or not.
        self.gettransportplan = gettransportplan

        # Make a cell to start the graph.  Use the first point as the root
        # if none is given.
        P = iter(M)
        root_center = root or next(P)
        root_cell = self.Vertex(root_center)

        # Add the points to the root cell.
        # It doesn't matter if the root point is also in the list of points.
        # It will not be added twice.
        for i, p in enumerate(P):
            root_cell.addpoint(p)

        # Add the new cell as the one vertex of the graph.
        self.addvertex(root_cell)
        self.addedge(root_cell, root_cell)

        # The heap has been moved to GreedyNeighborGraph.
        # self.heap = MaxHeap([root_cell], key = lambda c: c.radius)

    def iscloseenoughto(self, p, q):
        """
        Return True iff the cells `p` and `q` are close enough to be neighbors.
        """
        return q.dist(p.center) <= p.radius + q.radius +\
            self.nbrconstant * max(p.radius, q.radius)

    def addcell(self, newcenter, parent):
        """
        Add a new cell centered at `newcenter` and also compute the mass moved
        by this change to the neighbor graph.

        The `parent` is a sufficiently close cell that is already in the
        graph.
        It is used to find nearby cells to be the neighbors.
        The cells are rebalanced with points moving from nearby cells into
        the new cell if it is closer.

        If self.gettransportplan=True this method also returns a dictionary
        of the number of points gained and lost by every cell (indexed by
        center) in this change to the neighbor graph.
        """
        # Create the new cell.
        newcell = self.Vertex(newcenter)

        # Create transportation plan for adding this cell
        transportplan = DefaultDict(int)

        # Make the cell a new vertex.
        self.addvertex(newcell)
        self.addedge(newcell, newcell)

        # Rebalance the new cell.
        for nbr in self.nbrs(parent):
            localtransport = self.rebalance(newcell, nbr)
            # Add change caused by this rebalance to transportation plan if
            # requested.
            if localtransport != 0 and self.gettransportplan:
                transportplan[newcenter] += localtransport
                transportplan[nbr.center] -= localtransport

            # The heap update has been delegated to the GreedyNeighborGraph.
            # self.heap.changepriority(nbr)

        # Add neighbors to the new cell.
        for newnbr in self.nbrs_of_nbrs(parent):
            if self.iscloseenoughto(newcell, newnbr):
                self.addedge(newcell, newnbr)

        # After all the radii are updated, prune edges that are too long.
        for nbr in set(self.nbrs(parent)):
            self.prunenbrs(nbr)

        # The following update has moved to the GreedyNeighborGraph
        # self.heap.insert(newcell)

        # If self.gettransportplan=False this method returns an empty
        # transportplan
        return newcell, transportplan

    def rebalance(self, a, b):
        """
        Returns the number of points moved from `b` to `a`.

        Move points from the cell `b` to the cell `a` if they are
        sufficiently closer to `a.center`.
        """
        points_to_move =\
            {p for p in b.points if a.comparedist(p, b, self.moveconstant)}
        b.points -= points_to_move
        mass_to_move = 0
        for p in points_to_move:
            a.addpoint(p)
            mass_to_move += self.mass[p]
        # The radius of self (`a`) is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        b.updateradius()
        return mass_to_move

    def nbrs_of_nbrs(self, u):
        return {b for a in self.nbrs(u) for b in self.nbrs(a)}

    def prunenbrs(self, u):
        """
        Eliminate neighbors that are too far with respect to the current
        radius.
        """
        nbrs_to_delete = set()
        for v in self.nbrs(u):
            if not self.iscloseenoughto(u, v):
                nbrs_to_delete.add(v)

        # Prune the excess edges.
        for v in nbrs_to_delete:
            self.removeedge(u, v)

    def cellmass(self, cell):
        """
        Method to compute the number of points with multiplicity in a cell.
        Better to use this than `len(cell)`.
        """
        return sum(self.mass[p] for p in cell)


class GreedyNeighborGraph(NeighborGraph):
    def __init__(self,
                 M,
                 root=None,
                 nbrconstant=1,
                 moveconstant=1,
                 gettransportplan=False,
                 mass=None):
        super().__init__(M, root, nbrconstant, moveconstant, gettransportplan,
                         mass)

        # The root cell should be the only vertex in the graph.
        root_cell = next(iter(self._nbrs))
        self.heap = MaxHeap([root_cell], key=lambda c: c.radius)

    def addcell(self, newcenter, parent):
        newcell, transportplan = super().addcell(newcenter, parent)
        # Add `newcell` to the heap.
        self.heap.insert(newcell)

        return newcell, transportplan

    def rebalance(self, a, b):
        mass_to_move = super().rebalance(a, b)
        # Update the heap priority for `b`.
        self.heap.changepriority(b)

        return mass_to_move
