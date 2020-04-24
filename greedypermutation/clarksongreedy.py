from greedypermutation.clustergraph import Cluster, ClusterGraph
from greedypermutation.maxheap import MaxHeap

def greedy(M, seed = None):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.
    """
    for p, i in greedytree(M, seed):
        yield p

def greedytree(M, seed = None):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    # If no seed is provided, use the first point.
    G = ClusterGraph(M, seed or next(iter(M)))
    H = G.heap
    root = H.findmax()
    # Yield the first point.
    yield root.center, None

    # Store the indices of the previous points.
    index = {root : 0}

    for i in range(1, len(M)):
        cluster = H.findmax()
        point = cluster.pop()
        newcluster = G.addcluster(point, cluster)
        index[newcluster] = i
        yield point, index[cluster]
