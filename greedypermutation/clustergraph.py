from ds2.graph import Graph
# from ds2.priorityqueue import PriorityQueue
from greedypermutation.maxheap import MaxHeap

class Cluster:
    def __init__(self, center):
        """
        Create a new cluster with the given `center`.

        A new cluster only contains a single point, its center.
        """
        self.points = {center}
        self.center  = center
        self.radius = 0

    def addpoint(self, p):
        """
        Add the point `p` to the cluster.
        """
        self.points.add(p)
        self.radius = max(self.radius, self.dist(p))

    def dist(self, point):
        """
        Return the distance between the centers of `self` and `other`.  Note,
        this allows `Cluster` to be treated like a point.
        """
        return self.center.dist(point)

    def updateradius(self):
        """
        Set the radius of the cluster to be the farthest distance from a point
        to the center.
        """
        self.radius = max((self.dist(p) for p in self.points), default = 0)

    def pop(self):
        """
        Remove and return the farthest point in the cluster.

        Returns `None` if there there are no points other than the center.
        """
        if len(self) == 1:
            return None
        p = max(self.points, key = self.dist)
        # This is linear time!  We should maybe use a heap here.
        # However, the pop is followed by an update that will iterate over all
        # the points anyway.
        self.points.remove(p)
        self.updateradius()
        return p

    def rebalance(self, other):
        """
        Move points from the cluster `other` to the cluster `self` if they are
        closer to the `self` center.
        """
        pts_to_move = {p for p in other.points if self.dist(p) < other.dist(p)}
        other.points -= pts_to_move
        for p in pts_to_move:
            self.addpoint(p)
        # The radius of self is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        other.updateradius()

    def iscloseenoughto(self, other):
        return other.dist(self.center) <= self.radius + other.radius + \
            max(self.radius, other.radius)

    def __len__(self):
        """
        Return the total number of points in the cluster, including the center.
        """
        return len(self.points)

    def __lt__(self, other):
        """
        Clusters are ordered by their radii.
        """
        return self.radius > other.radius

    def __repr__(self):
        return str(self.center)

class ClusterGraph(Graph):
    # Initialize it as an empty graph.
    def __init__(self, points, root = None):
        """
        Initialize a new ClusterGraph.

        It starts with an iterable of points.  The first point will be the
        center of the default cluster and all other points will be placed
        inside.
        """
        # Initialize the `ClusterGraph` to be a `Graph`.
        Graph.__init__(self)
        P = iter(points)
        # Make a cluster to start the graph.  Use the first point as the root
        # if none is give.
        root_cluster = Cluster(root or next(P))
        # Add the points to the root cluster.
        # It doesn't matter if the root point is also in the list of points.
        # It will not be added twice.
        for p in P:
            root_cluster.addpoint(p)
        # Add the new cluster as the one vertex of the graph.
        self.addvertex(root_cluster)
        self.addedge(root_cluster, root_cluster)
        self.heap = MaxHeap([root_cluster], key = lambda c: c.radius)


    def addcluster(self, newcenter, parent):
        """
        Add a new cluster centered at `newcenter`.

        The `parent` is a suffciently close cluster that is already in the
        graph.
        It is used to find nearby clusters to be the neighbors.
        The clusters are rebalanced with points moving from nearby clusters into
        the new cluster if it is closer.
        """
        # Create the new cluster.
        newcluster = Cluster(newcenter)
        # Make the cluster a new vertex.
        self.addvertex(newcluster)
        self.addedge(newcluster, newcluster)

        # Rebalence the new cluster.
        for nbr in self.nbrs(parent):
            newcluster.rebalance(nbr)
            self.heap.changepriority(nbr)

        # Find potential new neighbors
        nbrs = self.nbrs(parent)
        potential_nbrs = set(self.nbrs(parent))
        # nbrs_of_nbrs = set()
        for a in nbrs:
            for b in self.nbrs(a):
                potential_nbrs.add(b)
        # potential_nbrs = nbrs | nbrs_of_nbrs

        # Add neighbors to the new cluster.
        for newnbr in potential_nbrs:
            if newcluster.iscloseenoughto(newnbr):
                self.addedge(newcluster, newnbr)

        # self.heap.insert(newcluster)
        return newcluster

    def closenbrs(self, u):
        """ Return the neighbors of u in the cluster graph.

        The neighbors are autoamtically pruned to only include those that are
        sufficiently close with respect to their radii.
        """
        nbrs_to_delete = set()
        for v in self.nbrs(u):
            if u.iscloseenoughto(v):
                yield v
            else:
                nbrs_to_delete.add(v)

        # Prune the excess edges.
        for v in nbrs_to_delete:
            self.removeedge(u,v)
