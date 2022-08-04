from collections import defaultdict
from greedypermutation.neighborgraph import GreedyNeighborGraph


def knnsample(M, k, seed=None):
    # If no seed is provided, use the first point.
    G = GreedyNeighborGraph(M, seed, 2, 1)
    markednbrs = defaultdict(set)
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center

    for i in range(1, len(M)):
        cell = H.findmax()
        point = cell.farthest
        if point is None:
            break
        cell.points.remove(point)
        cell.updateradius()

        radius = 2 * M.dist(point, cell.center)

        nearbypts = {
                     q for nbr in G.nbrs(cell)
                     for q in nbr
                     if M.dist(q, point) <= radius
                    }

        nearbymarkedpts = {
                           q for q in markednbrs.get(point, ())
                           if M.dist(q, point) <= radius
                          }

        # Check if the distance to k points in M is at least twice the
        # distance to the nearest point in the output.
        # If there are fewer than k nearby points, we mark it.
        # If there are at least k, we yield it and add the cell.
        if len(nearbypts) + len(nearbymarkedpts) < k:
            for p in nearbypts:
                # This is overkill.  Should only add this if point is less than
                # twice the distance to RNN(p)
                markednbrs[p].add(point)
            # In greedy, `addcell` updates the heap after moving points.
            # Here, we have to do it manually.
            H.changepriority(cell)
        else:
            if point in markednbrs:
                del markednbrs[point]
            G.addcell(point, cell)
            yield point


def knnsample_brute_force(M, k):
    """
    A brute force implementation of the knnsampling algorithm.

    The point is to use this as a reference implementation.
    """
    seed = M[0]
    S = [seed]
    yield seed
    d_Mk = {p: p.dist(sorted(M, key=p.dist)[k]) for p in M}
    d_S1 = {p: p.dist(seed) for p in M}
    not_done_yet = True
    while not_done_yet:
        not_done_yet = False
        for p in M:
            if d_Mk[p] < 2 * d_S1[p]:
                S.append(p)
                yield p
                for q in M:
                    d_S1[q] = min(d_S1[q], q.dist(p))
                not_done_yet = True
