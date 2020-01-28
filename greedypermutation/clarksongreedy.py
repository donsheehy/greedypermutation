from .metricspace import MetricSpace
from .point import Point
from .clustergraph import Cluster, ClusterGraph

def greedy(M, seed = None):
    for p, i in greedytree(M, seed):
        yield p

def greedytree(M, seed = None):
    """ Return a greedy tree of points in # XXX:
    """
    # If no seed is provided, use the first point.
    G = ClusterGraph(M, seed or next(iter(M)))
    H = G.heap
    root = H.findmax()
    # Yield the first point.
    yield root.center, None

    # Keep track of the number fo points yielded so far.
    count = 0
    # Store the indices of the previous points
    index = {root : 0}

    while H:
        cluster = H.removemax()
        point = cluster.pop()
        yield point, index[cluster]

        newcluster = G.addcluster(point, cluster)
        index[newcluster] = count + 1
        count += 1

        # Update the heap
        if newcluster.radius > 0:
            H.insert(newcluster)
        if cluster.radius > 0:
            H.insert(cluster)
