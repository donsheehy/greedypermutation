import logging
from ds2.graph import Graph
from metricspaces import metric_class, MetricSpace
from greedypermutation.maxheap import MaxHeap
from greedypermutation.fvm.utils import TreeParameters
from greedypermutation.fvm.bucketqueue import BucketQueue


@metric_class
class Cell:
    def __init__(self, x):
        """
        Create a new cell with the given center `x.center`.
        """
        # logging.debug(f"Creating cell with center {x}.")
        self.center = x
        self.points = set()
        self.outradius = 0
        self.farthest = None

    def tidy(self):
        """
        Tidies the cell and updates the radius.
        """
        if not hasattr(self, "tidy_param"):
            logging.error(
                f"Tidying cell with center {self.center} and {len(self.points)} nodes."
            )
            raise RuntimeError("Cannot tidy a cell without a tidying parameter")
        self.update_farthest()
        x = self.farthest
        while x.radius > (self.tidy_param - 1) * self.dist(x.center):
            self.split_node(x)
            self.update_farthest()
            x = self.farthest
        # logging.debug(
        #     f"Tidy cell with center {self.center} has {self.num_nodes()} nodes containing {len(self)} points and outradius {self.outradius}."
        # )

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
        # SID: x is a node.
        self.points.add(x)

    def removepoint(self, x):
        if x not in self.points:
            logging.error(f"Trying to point {x.center} from cell {self.center}.")
            raise RuntimeError("Trying to remove non-existent point from a cell!")
        self.points.remove(x)

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

    def move(self, x, other):
        """
        Check if `x` can move to new cell `other`.
        """
        return (
            self.move_param * (other.dist(x.center) + x.radius)
            <= self.dist(x.center) - x.radius
        )

    def stay(self, x, other):
        """
        Check if `x` can stay.
        """
        return (
            self.nbr_param * (other.dist(x.center) - x.radius)
            >= self.dist(x.center) + x.radius
        )

    def split_before_move(self, to_split):
        """
        Replace the nodes in `to_split` by their children.
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
            logging.error(
                f"Splitting leaf with center {x.center} in cell {self.center}."
            )
            raise RuntimeError("Splitting a leaf")
        self.points.remove(x)
        self.points.add(x.left)
        self.points.add(x.right)
    def num_nodes(self):
        return len(self.points)

    def __len__(self):
        """
        Return the total number of points in the cell, including the center.
        """
        return sum(len(p) for p in self.points)

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
    def __init__(self, G, nbr_const=1, move_const=1, tidy_const=1, space=None):
        # Initialize the `NeighborGraph` to be a `Graph`.
        super().__init__()

        if nbr_const < move_const:
            logging.error(
                f"Passed nbr constant {nbr_const} and move constant {move_const}."
            )
            raise RuntimeError(
                "The move constant must not be larger than the neighbor constant."
            )

        if move_const < tidy_const:
            logging.error(
                f"Passed move constant {move_const} and tidy constant {tidy_const}."
            )
            raise RuntimeError(
                "The tidying constant must not be larger than the move constant."
            )
        
        if space is None:
            space = MetricSpace([G[0].center])
        self.nbrconstant = nbr_const
        self.moveconstant = move_const
        self.tidyconstant = tidy_const

        # Establish a class for the cells.
        self.Vertex = Cell(space)
        self.Vertex.tidy_param = self.tidyconstant
        self.Vertex.move_param = self.moveconstant
        self.Vertex.nbr_param = self.nbrconstant

        # Make a cell to start the graph.
        root_center = G[0].center
        root_cell = self.Vertex(root_center)

        for g in G:
            root_cell.addpoint(g)
        root_cell.tidy()
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
        # Tidy the new cell after points have moved into it.
        newcell.tidy()

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

        to_move, to_split, to_check = set(), set(), b.points
        while to_check == b.points or len(to_split) > 0:
            if len(to_split) > 0:
                to_check = b.split_before_move(to_split)
                to_split = set()
            for p in to_check:
                if b.move(p, a):
                    to_move.add(p)
                elif b.stay(p, a):
                    continue
                else:
                    if p.isleaf():
                        logging.error(
                            f"Splitting leaf {p.center} with radius {p.radius} when moving points from {b.center} to {a.center}."
                        )
                        logging.error(
                            f"Cannot move because {self.moveconstant*(a.dist(p.center) + p.radius)} = {self.moveconstant}*({a.dist(p.center)} + {p.radius}) > {b.dist(p.center)} - {p.radius} = {b.dist(p.center) - p.radius}"
                        )
                        logging.error(
                            f"Cannot stay because {self.nbrconstant*(a.dist(p.center) - p.radius)} = {self.nbrconstant}*({a.dist(p.center)} - {p.radius}) < {b.dist(p.center)} + {p.radius} = {b.dist(p.center) + p.radius}"
                        )
                        raise RuntimeError("Splitting a leaf!")
                    to_split.add(p)
            to_check = set()

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

    def __init__(self, G, params=TreeParameters(1,1,1,1), space=None):
        move_const, nbr_const, tidy_const, bucket_size = params
        super().__init__(G, nbr_const, move_const, tidy_const, space)

        # The root cell should be the only vertex in the graph.
        root_cell = next(iter(self._nbrs))
        if bucket_size > 1:
            self.heap = BucketQueue(
                [root_cell], key=lambda c: c.outradius, bucket_size=bucket_size
            )
        else:
            self.heap = MaxHeap([root_cell], key=lambda c: c.outradius)

    def addcell(self, newcenter, parent):
        newcell = super().addcell(newcenter, parent)
        # Add `newcell` to the heap.
        self.heap.insert(newcell)
        # logging.debug(f"Inserted cell at center {newcenter}")
        return newcell

    def rebalance(self, a, b):
        super().rebalance(a, b)
        # Update the heap priority for `b`.
        self.heap.changepriority(b)
