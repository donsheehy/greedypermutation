from collections import defaultdict
from greedypermutation.clustergraph import ClusterGraph

def knnsample(M, k, seed = None):
    # If no seed is provided, use the first point.
    G = ClusterGraph(M, seed, 2, 1)
    markednbrs = defaultdict(set)
    H = G.heap
    root = H.findmax()

    # Yield the first point.
    yield root.center

    for i in range(1, len(M)):
        cluster = H.findmax()
        point = cluster.pop()
        radius = 2 * point.dist(cluster.center)

        nearbypts = {q for nbr in G.nbrs(cluster)
                       for q in nbr
                       if q.dist(point) <= radius
                    }

        nearbymarkedpts = {q for q in markednbrs.get(point, ())
                             if q.dist(point) <= radius
                          }

        # If there are fewer than k nearby points, we mark it.
        # If there are at least k, we yield it and add the cluster.
        if len(nearbypts) + len(nearbymarkedpts) < k:
            for p in nearbypts:
                # This is overkill.  Should only add this if point is less than
                # twice the distance to RNN(p)
                markednbrs[p].add(point)
            # In greedy, `addcluster` updates the heap after moving points.
            # Here, we have to do it manually.
            H.changepriority(cluster)
        else:
            if point in markednbrs:
                del markednbrs[point]
            newcluster = G.addcluster(point, cluster)
            yield point
