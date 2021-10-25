from greedypermutation.neighborgraph import Cell, NeighborGraph
from greedypermutation import GreedyTree

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

def _onehopgreedy(M, seed = None, alpha = 1/3):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a one-hop greedy permutation and `index` is the index
    of the nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    # If no seed is provided, use the first point.
    T = GreedyTree(M)
    G = NeighborGraph(M, seed or next(iter(M)))
    H = G.heap
    root = H.findmax()
    # Yield the first point.
    yield root.center, None

    # Store the indices of the previous points.
    index = {root : 0}

    for i in range(1, len(M)):
        cell = H.findmax()
        x = max(cell, key = cell.dist)
        r = x.dist(cell.center)
        ra = r * alpha
        potentials = (
            (q,n)
            for n in G.nbrs(cell)
            for q in n
            if x.dist(q) < ra
        )
        def rangesample(qn):
            q, n = qn
            # TODO: replace with rangecount ?
            return len(list(T.range(q, ra, ra/10)))
        point, parent = max(potentials, key = rangesample)
        newcell, transportplan = G.addcell(point, parent)
        index[newcell] = i
        yield point, index[parent]
