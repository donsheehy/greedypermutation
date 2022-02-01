from email.errors import NonPrintableDefect
from typing import DefaultDict


def greedy(M, seed = None, tree = False, gettransportplan=False, mass=None):
    """
    Return an iterator that yields the points of `M` ordered by a greedy
    permutation.

    The optional `seed` parameter indicates the point that should appear first.

    The `tree` parameter is a flag to set whether or not to return also the
    nearest predecessors in the pairing (thus giving the tree).  If set to
    `True`, the result will iterate over `(point, index)` pairs.

    When `gettransportplan` is set to True `_greedy` returns a dictionary of mass
    moved in each step of the greedy permutation.
    """
    if tree and gettransportplan:
        yield from _greedy(M, seed, gettransportplan, mass)
    elif tree:
        for p, i, t in _greedy(M, seed, gettransportplan, mass):
            yield p, i
    elif gettransportplan:
        for p, i, t in _greedy(M, seed, gettransportplan, mass):
            yield p, t
    else:
        for p, i, t in _greedy(M, seed, gettransportplan, mass):
            yield p

def _greedy(M, seed = None, gettransportplan=False, mass=None):
    """
    Return an iterator that yields `(point, index)` pairs, where `point`
    is the next point in a greedy permutation and `index` is the index of they
    nearest predecessor.

    The optional `seed` parameter indicates the point that should appear first.
    """
    P = list(M)

    if mass is None:
        mass = [1]*len(M)
    elif len(mass) != len(M):
        raise ValueError("`mass` must of same length as `M`")
    # If no seed is provided, use the first point.
    if seed is None:
        seed = P[0]
    else:
        # Put the seed in the first position.
        seed_index = P.index(seed)
        P[0], P[seed_index] = P[seed_index], P[0]
    n = len(P)
    transportplan = DefaultDict(int)
    if gettransportplan:
        transportplan[P[0]] = sum(mass)
    yield P[0], None, transportplan
    pred = {p:0 for p in P}
    preddist = {p: M.dist(p, P[pred[p]]) for p in P}
    for i in range(1,n):
        transportplan = DefaultDict(int)
        farthest = i
        for j in range(i+1, n):
            if preddist[P[j]] > preddist[P[farthest]]:
                farthest  = j
        P[i], P[farthest] = P[farthest], P[i]
        if gettransportplan:
            transportplan[P[pred[P[i]]]] -= mass[i]
            transportplan[P[i]] += mass[i]
        # Update the predecessor distance if necessary.
        for j in range(i+1, n):
            newdistance = M.dist(P[i], P[j])
            if newdistance < preddist[P[j]]:
                if gettransportplan:
                    transportplan[P[pred[P[j]]]] -= mass[j]
                    transportplan[P[i]] += mass[j]
                pred[P[j]] = i
                preddist[P[j]] = newdistance
        yield P[i], pred[P[i]], transportplan
