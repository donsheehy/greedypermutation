import logging
from ds2.graph import Graph
from metricspaces import metric_class, MetricSpace
from greedypermutation.maxheap import MaxHeap

@metric_class
class Cell:
    def __init__(self, x):
        """
        Create a new cell with the given center `x.center`.
        """
        # SID: tidying requires that points be stored in a heap.
        # SID: Set is better than heap. Need to implement get max.
        logging.info(
            f"Creating cell with center {(x.center.x, x.center.y)} and {len(x)} points."
        )
        self.center = x.center
        self.points = {x}
        self.outradius = 0
        self.tidy()

    def tidy(self):
        """
        Tidies the cell and updates the radius.
        """
        logging.info(
            f"Tidying cell with center {self.center} and {len(self.points)} nodes."
        )
        self.update_farthest()
        x = self.farthest
        while x.radius > (self.tidy_param - 1) * self.dist(x.center):
            self.split_node(x)
            self.update_farthest()
            x = self.farthest
        logging.info(
            f"Tidy cell with center {self.center} has {len(self.points)} nodes containing {sum(len(x) for x in self.points)} points and outradius {self.outradius}."
        )

    def update_farthest(self):
        """
        Update the out-radius.
        Update the node determining out-radius.
        """
        self.outradius = -1
        for x in self.points:
            if self.dist(x.center) + x.radius > self.outradius:
                self.outradius = self.dist(x.center) + x.radius
                self.farthest = x

    def addpoint(self, x):
        """
        Add the point `x` to the cell.
        """
        # SID: Now p is a node.
        # The node has to be tidy before updating the radius.
        self.points.add(x)
        self.tidy()

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
        return self.metric.comparedist(point, self.center, other.center, alpha=alpha)

    def move(self, x, other, alpha):
        """
        Check if `x` can move to new cell `other`.
        """
        # logging.info(f"Move if {other.dist(x.center)} + {x.radius} <= {self.dist(x.center)} - {x.radius}")
        return (
            alpha * (other.dist(x.center) + x.radius) < self.dist(x.center) - x.radius
        )

    def stay(self, x, other, beta):
        """
        Check if `x` can stay.
        """
        # logging.info(f"Stay if {other.dist(x.center)} - {x.radius} <= {self.dist(x.center)} + {x.radius}")
        return (
            beta * (other.dist(x.center) - x.radius) >= self.dist(x.center) + x.radius
        )

    def split_before_move(self, to_split):
        """
        Replace the points in to_split by their children.
        """
        split_nodes = set()
        for x in to_split:
            self.split_node(x)
            split_nodes |= {x.left, x.right}
        # Also return these points.
        return split_nodes

    def split_node(self, x):
        """
        Replace node by its children in the same cell.
        """
        if x.isleaf():
            raise ValueError("Splitting a leaf")
        self.points.remove(x)
        self.points.add(x.left)
        self.points.add(x.right)

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
        Cells are ordered by their outradii.
        """
        return self.outradius > other.outradius

    def __repr__(self):
        return str(self.center)


class NeighborGraph(Graph):
    def __init__(self, G, nbr_const=1, move_const=1, tidy_const=1, bucket_size=1):
        # Initialize the `NeighborGraph` to be a `Graph`.
        super().__init__()

        # if nbrconstant < moveconstant:
        #     raise RuntimeError(
        #         "The move constant must not be larger than the" "neighbor constant."
        #     )
        self.nbrconstant = nbr_const
        self.moveconstant = move_const
        self.tidyconstant = tidy_const
        self.bucketsize = bucket_size

        # Establish a class for the cells.
        self.Vertex = Cell(MetricSpace([G[0].center]))
        self.Vertex.tidy_param = self.tidyconstant

        # Make a cell to start the graph.
        root_center = G[0]
        root_cell = self.Vertex(root_center)

        for i, g in enumerate(G[1:]):
            root_cell.addpoint(g)

        # Add the new cell as the one vertex of the graph.
        self.addvertex(root_cell)
        self.addedge(root_cell, root_cell)

    def iscloseenoughto(self, p, q):
        """
        Return True iff the cells `p` and `q` are close enough to be neighbors.
        """
        return q.dist(p.center) <= p.outradius + q.outradius + self.nbrconstant * max(
            p.outradius, q.outradius
        )

    def addcell(self, newcenter, parent):
        """
        Add a new cell centered at `newcenter`.

        The `parent` is a sufficiently close cell that is already in the
        graph.
        It is used to find nearby cells to be the neighbors.
        The cells are rebalanced with points moving from nearby cells into
        the new cell if it is closer.
        """
        # Remove the point from the parent.
        parent.points.remove(newcenter)
        # Create the new cell.
        newcell = self.Vertex(newcenter)

        # Make the cell a new vertex.
        self.addvertex(newcell)
        self.addedge(newcell, newcell)

        # Move points to the new cell.
        for nbr in self.nbrs(parent):
            self.rebalance(newcell, nbr)
            # The heap update has been delegated to the GreedyNeighborGraph.
            # self.heap.changepriority(nbr)

        # Add neighbors to the new cell.
        for newnbr in self.nbrs_of_nbrs(parent):
            if self.iscloseenoughto(newcell, newnbr):
                self.addedge(newcell, newnbr)

        # After all the radii are updated, prune edges that are too long.
        for nbr in set(self.nbrs(parent)):
            self.prunenbrs(nbr)

        return newcell

    def rebalance(self, a, b):
        """
        Move points from the cell `b` to the cell `a` if they are
        sufficiently closer to `a.center`.
        """
        # SID: Determining points to move will be different now.
        # The points are nodes.
        # They have to be split-on-move for merge, not for refine.
        # Maybe work out the constants so that this is taken care of in the call itself.

        to_move, to_split = set(), set()
        points_to_check = b.points
        while points_to_check == b.points or len(to_split) > 0:
            if len(to_split) > 0:
                points_to_check = b.split_before_move(to_split)
                to_split = set()
            for p in points_to_check:
                if b.move(p, a, self.moveconstant):
                    to_move.add(p)
                elif b.stay(p, a, self.nbrconstant):
                    continue
                else:
                    to_split.add(p)
            points_to_check = set()

        logging.info(
            f"Moving {len(to_move)} points from cell with center {b.center} to cell {a.center}."
        )
        b.points -= to_move
        for p in to_move:
            a.addpoint(p)
        # The out-radius of self (`a`) is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        # SID: Tidy the cell before updating out-radius
        b.tidy()

    def nbrs_of_nbrs(self, u):
        """
        Returns nbrs of nbrs of u.
        """
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


class GreedyNeighborGraph(NeighborGraph):
    """_summary_

    Parameters
    ----------
    NeighborGraph : _type_
        _description_
    """

    def __init__(self, G, nbr_const=1, move_const=1, tidy_const=1, bucket_size=1):
        super().__init__(G, nbr_const, move_const, tidy_const, bucket_size)

        # The root cell should be the only vertex in the graph.
        root_cell = next(iter(self._nbrs))
        # SID: This heap will have to be a bucket queue.
        self.heap = MaxHeap([root_cell], key=lambda c: c.outradius)

    def addcell(self, newcenter, parent):
        logging.info(f"Adding cell with center {newcenter} and parent {parent.center}.")
        newcell = super().addcell(newcenter, parent)
        logging.info(f"Cell inserted succesfully, outradius {newcell.outradius}.")
        # Add `newcell` to the heap.
        self.heap.insert(newcell)

        return newcell

    def rebalance(self, a, b):
        super().rebalance(a, b)
        # Update the heap priority for `b`.
        self.heap.changepriority(b)
