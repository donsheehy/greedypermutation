from greedypermutation.neighborgraph import Cell, NeighborGraph

def greedy(M, seed = None, nbrconstant = 1, moveconstant=1, tree = False, gettransportplan=False, mass=None):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The optional `nbrconstant` and `moveconstant` parameters set the approximation
    in the `NeighborGraph`. If both parameters are equal to 'alpha', then every
    point will have a parent that is a `1/alpha` approximate nearest neighbor.  The
    resulting greedy permutation will be a `1/alpha` approximation.

    The `gettransportplan` parameter sets the corresponding flag in NeighborGraph which
    when set returns a dictionary of mass moved in each step of the greedy permutation.
    """
    if tree and gettransportplan:
        yield from _greedy(M, seed, nbrconstant, moveconstant, gettransportplan, mass)
    elif tree:
        for p, i, t in _greedy(M, seed, nbrconstant, moveconstant, gettransportplan, mass):
            yield p, i
    elif gettransportplan:
        for p, i, t in _greedy(M, seed, nbrconstant, moveconstant, gettransportplan, mass):
            yield p, t
    else:
        for p, i, t in _greedy(M, seed, nbrconstant, moveconstant, gettransportplan, mass):
            yield p

def _greedy(M, seed = None, nbrconstant = 1, moveconstant=1, gettransportplan=False, mass=None):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    if not M:
        return
    # If no seed is provided, use the first point.
    G = NeighborGraph(M, seed or next(iter(M)), nbrconstant, moveconstant, gettransportplan, mass)
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center, None, {root.center: G.cellmass(root)}

    # Store the indices of the previous points.
    index = {root : 0}

    for i in range(1, len(M)):
        cell = H.findmax()
        point = cell.pop()
        newcell, transportplan = G.addcell(point, cell)
        index[newcell] = i
        yield point, index[cell], transportplan
