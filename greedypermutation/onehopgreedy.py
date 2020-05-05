from greedypermutation.clustergraph import Cluster, ClusterGraph

def onehopgreedy(M, seed = None, tree = False):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.
    """
    if tree:
        yield from _onehopgreedy(M, seed)
    else:
        for p, i in _onehopgreedy(M, seed):
            yield p

def _onehopgreedy(M, seed = None):
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
        x = max(cluster, key = cluster.dist)
        potentials = (
            (q,n)
            for n in G.nbrs(cluster)
            for q in n
            if x.dist(q) < n.dist(q)
        )
        point, parent = max(potentials, key = lambda qn: x.dist(qn[0]))
        newcluster = G.addcluster(point, parent)
        index[newcluster] = i
        yield point, index[parent]
