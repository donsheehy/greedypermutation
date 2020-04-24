from greedypermutation.clustergraph import ClusterGraph, Cluster

class kNNCluster(Cluster):
    def iscloseenoughto(self, other):
        return other.dist(self.center) <= self.radius + other.radius + \
            2 * max(self.radius, other.radius)

class kNNClusterGraph(ClusterGraph):
    Vertex = kNNCluster

def knnsample(M, k, seed = None):
    # If no seed is provided, use the first point.
    G = kNNClusterGraph(M, seed or next(iter(M)))
    H = G.heap
    root = H.findmax()
    # Yield the first point.
    yield root.center

    markednbrs = {}

    for i in range(1, len(M)):
        cluster = H.findmax()
        point = cluster.pop()
        nearbypts = set()
        radius = 2 * point.dist(cluster.center)

        for nbr in G.nbrs_of_nbrs(cluster):
            for q in nbr.points:
                if q.dist(point) <= radius:
                    nearbypts.add(q)
        nearbymarkedpts = {q for q in markednbrs.get(point, ())
                                if q.dist(point) <= radius}
        # If there are fewer than k nearby points, we mark it.
        # If there are at least k, we yield it and add the cluster.
        if len(nearbypts) + len(nearbymarkedpts) < k:
            for p in nearbypts:
                # This is overkill.  Should only add this if point is less than
                # twice the distance to RNN(p)
                markednbrs.get(p, set()).add(point)
            # In greedy, `addcluster` updates the heap after moving points.
            # Here, we have to do it manually.
            H.changepriority(cluster)
        else:
            if point in markednbrs:
                del markednbrs[point]
            newcluster = G.addcluster(point, cluster)
            yield point
