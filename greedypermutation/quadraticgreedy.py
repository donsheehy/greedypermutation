def greedy(M, seed = None):
    """ Return an iterator that yields the points of `M` ordered by a greedy
    permutation.
    """
    for p, i in greedytree(M, seed):
        yield p

def greedytree(M, seed = None):
    """ Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.
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
