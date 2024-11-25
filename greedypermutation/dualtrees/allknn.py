from collections import defaultdict
from greedypermutation.maxheap import MaxHeap
from greedypermutation.knnheap import KNNHeap
from greedypermutation.dualtrees.traversal import dualtree_search, dualtree_analysis
from greedypermutation.dualtrees.viabilitygraph import ViabilityGraph


# def all_knn(A, B, k, epsilon=0):
#     # def absorb(a):
#     #     nbrhood = {b for b in G.A[a]}
#     #     for b in nbrhood:
#     #         if a.dist(b.center) < rng - a.radius - b.radius:
#     #             G.remove_edge(a, b)
#     #             nbrs[a].add(b)
    
#     def update_candidates(a, ball):
#         if ball.left in G.B:
#             if ball in knn_heaps[a]:
#                 knn_heaps[a].refine(ball)
#             else:
#                 knn_heaps[a].insert(left)
#                 knn_heaps[a].insert(right)
#                 knn_heaps[a].tighten()

#     def prune(a):
#         nbrhood = {b for b in G.A[a]}
#         ub = knn_heaps[a].radius
#         for b in nbrhood:
#             if a.dist(b.center) > ub + 2*a.radius + b.radius:
#                 G.remove_edge(a, b)

#     def finish(a):
#         ub = knn_heaps[a].radius
#         farthest = knn_heaps[a].findmax()
#         lb = ub - 2*farthest.radius
#         if 2*a.radius <= lb - ub/(1+epsilon):
#             # absorb(a)
#             for p in a:
#                 out[p] = (ub + a.radius, farthest.center)

#     def update(a, ball):
#         # absorb(a)
#         update_candidates(a, ball)
#         prune(a)
#         finish(a)

#     H = MaxHeap([A,B], key=lambda x:x.radius)
#     G = ViabilityGraph(A,B)
#     out = defaultdict(set)
#     knn_heaps = {A: KNNHeap(A.center, k)}
#     knn_heaps[A].insert(B)
#     # nbrs = defaultdict(set)

#     for ball in H:
#         if ball.isleaf():
#             break
#         left, right = ball.left, ball.right

#         if ball in G.A:
#             # nbrs[left] = {b for b in nbrs[ball]}
#             # nbrs[right] = {b for b in nbrs[ball]}
#             # del nbrs[ball]
#             candidates = [b for b in knn_heaps.pop(ball, set())]
#             knn_heaps[left] = KNNHeap(left.center, k)
#             knn_heaps[right] = KNNHeap(right.center, k)
#             for b in candidates:
#                 knn_heaps[left].insert(b)
#                 knn_heaps[right].insert(b)
#             # del knn_heaps[ball]

#             for b in G.A.pop(ball):
#                 G.B[b].remove(ball)
#                 G.add_edges([(left, b), (right, b)])
#             affected = {left, right}
#         else:
#             for a in G.B.pop(ball):
#                 G.A[a].remove(ball)
#                 G.add_edges([(a, left), (a, right)])
#             affected = {a for a in G.B[left]}

#         for a in affected:
#             update(a, ball)

#         H.insert(left)
#         H.insert(right)
    
#     for a in G.A:
#         finish(a)

#     return out


def all_knn_setup(A, B, k, epsilon=0):
    # def absorb(a):
    #     nbrhood = {b for b in G.A[a]}
    #     for b in nbrhood:
    #         if a.dist(b.center) < rng - a.radius - b.radius:
    #             G.remove_edge(a, b)
    #             nbrs[a].add(b)
    
    def update_candidates(a, ball):
        left, right = ball.left, ball.right
        if left in G.B:
            if ball in knn_heaps[a]:
                knn_heaps[a].refine(ball)
            else:
                knn_heaps[a].insert(left)
                knn_heaps[a].insert(right)
                knn_heaps[a].tighten()

    def prune(a):
        nbrhood = {b for b in G.A[a]}
        ub = knn_heaps[a].radius
        for b in nbrhood:
            if a.dist(b.center) > ub + 2*a.radius + b.radius:
                G.remove_edge(a, b)

    def finish(a):
        ub = knn_heaps[a].radius
        farthest = knn_heaps[a].findmax()
        lb = ub - 2*farthest.radius
        if 2*a.radius <= lb - ub/(1+epsilon):
            # absorb(a)
            for p in a:
                out[p] = (ub + a.radius, farthest.center)

    def init(ball):
        left, right = ball.left, ball.right
        # nbrs[left] = nbrs.pop(ball, set())
        # nbrs[right] = {b for b in nbrs[left]}
        candidates = [b for b in knn_heaps.pop(ball, set())]
        knn_heaps[left] = KNNHeap(left.center, k)
        knn_heaps[right] = KNNHeap(right.center, k)
        for b in candidates:
            knn_heaps[left].insert(b)
            knn_heaps[right].insert(b)
        
    def update(a, ball):
        update_candidates(a, ball)
        # absorb(a)
        prune(a)
        finish(a)

    def cleanup(a):
        finish(a)

    H = MaxHeap([A,B], key=lambda x:x.radius)
    G = ViabilityGraph(A,B)
    out = defaultdict(set)
    knn_heaps = {A: KNNHeap(A.center, k)}
    knn_heaps[A].insert(B)
    # nbrs = defaultdict(set)

    return G, H, init, update, cleanup, out, knn_heaps


def all_knn(A, B, k, epsilon=0):
    G, H, init, update, cleanup, out, _ = all_knn_setup(A, B, k, epsilon)
    dualtree_search(G, H, init, update, cleanup)
    return out


def all_knn_analyze(A, B, k, epsilon=0):
    G, H, init, update, cleanup, out, knn_heaps = all_knn_setup(A, B, k, epsilon)
    for _ in dualtree_analysis(G, H, init, update, cleanup):
        yield G, out, knn_heaps


if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = list(range(2,15,3))
    B = list(range(1,20,4))
    knn = 3

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], knn)
    print([b for b in B])
    output = all_knn(G_A, G_B, knn)
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')

    A = [1,2,3,6,7,8]
    B = [1,2,3,6,7,9]
    knn = 4

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], knn)
    print([b for b in B])
    output = all_knn(G_A, G_B, knn)
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')

    print("okay!")
