from greedypermutation.neighborgraph import Cell, GreedyNeighborGraph


def greedy(M,
           seed=None,
           nbrconstant=1,
           moveconstant=1,
           tree=False,
           pointtree=False,
           cell=None):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The optional `nbrconstant` and `moveconstant` parameters set the
    approximation in the `NeighborGraph`. If both parameters are equal to
    'alpha', then every point will have a parent that is a `1/alpha`
    approximate nearest neighbor.  The resulting greedy permutation will be a
    `1/alpha` approximation.

    The `pointtree` parameter indicates if the predecessor is yielded with each
    point.

    The `tree` parameter indicates if the index of the predecessor is yielded
    with each point.
    """
    G = GreedyNeighborGraph(M,
                            seed or next(iter(M)),
                            nbrconstant,
                            moveconstant,
                            cell)
    for p, c, i in _greedy(M, G):
        output = [p]
        if pointtree:
            output.append(c.center if c else None)
        if tree:
            output.append(i)
        yield output[0] if len(output) == 1 else tuple(output)


def _greedy(M, G):
    """
    Given a `MetricSpace` `M` and a `GreedyNeighborGraph` `G`, iterate over
    `(point, cell, index, transportplan)` tuples for greedy permutation of `M`.
    """
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center, None, None

    # Store the indices of the previous points.
    index = {root: 0}

    for i in range(1, len(M)):
        cell = H.findmax()
        point = cell.farthest
        newcell = G.addcell(point, cell)
        index[newcell] = i
        yield point, cell, index[cell]
