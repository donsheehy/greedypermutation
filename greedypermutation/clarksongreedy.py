from greedypermutation.clustergraph import Cluster, ClusterGraph

def greedy(M, seed = None, tree = False, alpha = 1):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The optional `alpha` parameter sets the approximation in the
    `ClusterGraph`.  Every point will have a parent that is a `1/alpha`
    approximate nearest neighbor.  The resulting greedy permutation will be a
    `1/alpha` approximation.
    """
    if tree:
        yield from _greedy(M, seed, alpha)
    else:
        for p, i in _greedy(M, seed, alpha):
            yield p

def _greedy(M, seed = None, alpha = 1):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    # If no seed is provided, use the first point.
    G = ClusterGraph(M, seed or next(iter(M)), alpha, alpha)
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
