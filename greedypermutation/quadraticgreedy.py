def greedy(M, seed = None, tree = False):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The `tree` parameter is a flag to set whether or not to return also the
    nearest predecessors in the pairing (thus giving the tree).  If set to
    `True`, the result will iterate over `(point, index)` pairs.
    """
    if tree:
        yield from _greedy(M, seed)
    else:
        for p, i in _greedy(M, seed):
            yield p

def _greedy(M, seed = None):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    P = list(M)

    # If no seed is provided, use the first point.
    if seed is None:
        seed = P[0]
    else:
        # Put the seed in the first position.
        seed_index = P.index(seed)
        P[0], P[seed_index] = P[seed_index], P[0]
    n = len(P)
    yield P[0], None
    pred = {p:0 for p in P}
    preddist = {p: M.dist(p, P[pred[p]]) for p in P}
    for i in range(1,n):
        farthest = i
        for j in range(i+1, n):
            if preddist[P[j]] > preddist[P[farthest]]:
                farthest  = j
        P[i], P[farthest] = P[farthest], P[i]
        # Update the predecessor distance if necessary.
        for j in range(i+1, n):
            newdistance = M.dist(P[i], P[j])
            if newdistance < preddist[P[j]]:
                pred[P[j]] = i
                preddist[P[j]] = newdistance
        yield P[i], pred[P[i]]
