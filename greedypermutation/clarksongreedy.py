from greedypermutation.neighborgraph import Cell, NeighborGraph

def greedy(M, seed = None, tree = False, nbrconstant = 1, moveconstant=1):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The optional `nbrconstant` and `moveconstant` parameters set the approximation
    in the `NeighborGraph`. If both parameters are equal to 'alpha', then every
    point will have a parent that is a `1/alpha` approximate nearest neighbor.  The
    resulting greedy permutation will be a `1/alpha` approximation.
    """
    if tree:
        yield from _greedy(M, seed, nbrconstant = nbrconstant, moveconstant = moveconstant)
    else:
        for p, i in _greedy(M, seed, nbrconstant = nbrconstant, moveconstant = moveconstant):
            yield p

def _greedy(M, seed = None, nbrconstant = 1, moveconstant=1):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    # If no seed is provided, use the first point.
    G = NeighborGraph(M, seed or next(iter(M)), nbrconstant = nbrconstant, moveconstant = moveconstant)
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center, None

    # Store the indices of the previous points.
    index = {root : 0}

    for i in range(1, len(M)):
        cell = H.findmax()
        point = cell.pop()
        newcell = G.addcell(point, cell)
        index[newcell] = i
        yield point, index[cell]
