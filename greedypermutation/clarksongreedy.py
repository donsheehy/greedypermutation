from greedypermutation.clustergraph import Cluster, ClusterGraph
from greedypermutation.maxheap import MaxHeap

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

    # Store the indices of the previous points
    index = {root : 0}

    for i in range(1, len(M)):
        cluster = H.findmax()
        point = cluster.pop()

        yield point, index[cluster]

        newcluster = G.addcluster(point, cluster)
        index[newcluster] = i

        # Update the heap
        H.insert(newcluster)
