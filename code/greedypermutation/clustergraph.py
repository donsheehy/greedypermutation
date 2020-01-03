from .graph import Graph
from heapq import heappush, heappop, heapify

class Cluster:
    def __init__(self, center):
        self.points = {center}
        self.center  = center
        self.radius = 0

    def addpoint(self, p):
        self.points.add(p)
        self.radius = max(self.radius, self.dist(p))

    def dist(self, point):
        return self.center.dist(point)

    def updateradius(self):
        self.radius = max((self.dist(p) for p in self.points), default = 0)

    def pop(self):
        """ Remove and return the farthest point in the cluster.
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
        """ Move points from other to self.
        """
        pts_to_move = {p for p in other.points if self.dist(p) < other.dist(p)}
        other.points -= pts_to_move
        for p in pts_to_move:
            self.addpoint(p)
        # The radius of self is automatically updated by addpoint.
        # The other radius needs to be manually updated.
        other.updateradius()

    def iscloseenoughto(self, other):
        return other.dist(self.center) < self.radius + other.radius + \
            max(self.radius, other.radius)

    def __len__(self):
        return len(self.points)

    # def key(self):
    #     """ The distance to the farthest point.
    #     """
    #     return self.radius

    def __lt__(self, other):
        """We reverse the order so that the min heap will serve as a max heap.
        """
        return self.radius > other.radius

class ClusterGraph(Graph):
    # Initialize it as an empty graph.
    def __init__(self, points):
        Graph.__init__(self)
        P = iter(points)
        root = Cluster(next(P))
        for p in P:
            root.addpoint(p)
        self.addvertex(root)

    def addcluster(self, newcenter, parent):
        # Create the new cluster.
        newcluster = Cluster(newcenter)
        # Make the cluster a new vertex.
        self.addvertex(newcluster)
        # Rebalence the new cluster.
        newcluster.rebalance(parent)
        for nbr in self.nbrs(parent):
            newcluster.rebalance(nbr)

        # Find potential new neighbors
        nbrs = self.nbrs(parent)
        potential_nbrs = set(self.nbrs(parent))
        # nbrs_of_nbrs = set()
        for a in nbrs:
            for b in self.nbrs(a):
                potential_nbrs |= b
        # potential_nbrs = nbrs | nbrs_of_nbrs

        # Add neighbors to the new cluster.
        for newnbr in potential_nbrs:
            if newcluster.iscloseenoughto(newnbr):
                self.addedge(newcluster, newnbr)

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
