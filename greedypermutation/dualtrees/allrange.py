from greedypermutation.maxheap import MaxHeap
from greedypermutation.dualtrees.traversal import dualtree_search, dualtree_analysis
from greedypermutation.dualtrees.viabilitygraph import ViabilityGraph
from collections import defaultdict


# def all_range(A, B, rng, epsilon=0):
#     def absorb(a):
#         # nonlocal G, rng, nbrs
#         nbrhood = {b for b in G.A[a]}
#         for b in nbrhood:
#             if a.dist(b.center) < rng - a.radius - b.radius:
#                 G.remove_edge(a, b)
#                 nbrs[a].add(b)
    
#     def prune(a):
#         # nonlocal G, rng
#         nbrhood = {b for b in G.A[a]}
#         for b in nbrhood:
#             if a.dist(b.center) > rng + a.radius + b.radius:
#                 G.remove_edge(a, b)

#     def finish(a):
#         # nonlocal G, rng, out, nbrs, ball
#         if len(G.A[a]) == 0 or ball.radius <= (epsilon / 4) * rng:
#             absorb(a)
#             for p in a:
#                 out[p] = nbrs[a]

#     def update(a):
#         absorb(a)
#         prune(a)
#         finish(a)

#     H = MaxHeap([A,B], key=lambda x:x.radius)
#     G = ViabilityGraph(A,B)
#     out = defaultdict(set)
#     nbrs = defaultdict(set)

#     for ball in H:
#         if ball.isleaf():
#             break
#         left, right = ball.left, ball.right

#         if ball in G.A:
#             nbrs[left] = nbrs.pop(ball, set())
#             nbrs[right] = {b for b in nbrs[left]}

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
#             update(a)

#         H.insert(left)
#         H.insert(right)
    
#     for a in G.A:
#         finish(a)

#     return out

# def all_range(A, B, rng, epsilon=0):
#     def absorb(a):
#         nbrhood = {b for b in G.A[a]}
#         for b in nbrhood:
#             if a.dist(b.center) < rng - a.radius - b.radius:
#                 G.remove_edge(a, b)
#                 nbrs[a].add(b)
    
#     def prune(a):
#         nbrhood = {b for b in G.A[a]}
#         for b in nbrhood:
#             if a.dist(b.center) > rng + a.radius + b.radius:
#                 G.remove_edge(a, b)

#     def finish(a, r):
#         if len(G.A[a]) == 0 or r <= (epsilon / 4) * rng:
#             absorb(a)
#             for p in a:
#                 out[p] = nbrs[a]

#     def update(a, ball):
#         absorb(a)
#         prune(a)
#         finish(a, ball.radius)

#     def init(ball):
#         left, right = ball.left, ball.right
#         nbrs[left] = nbrs.pop(ball, set())
#         nbrs[right] = {b for b in nbrs[left]}

#     def cleanup(a):
#         finish(a, 0)

#     out = defaultdict(set)
#     nbrs = defaultdict(set)
#     H = MaxHeap([A,B], key=lambda x:x.radius)
#     G = ViabilityGraph(A,B)

#     dualtree_search(G, H, init, update, cleanup)
#     return out


def all_range_setup(A, B, rng, epsilon):
    def absorb(a):
        nbrhood = {b for b in G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) < rng - a.radius - b.radius:
                G.remove_edge(a, b)
                nbrs[a].add(b)
    
    def prune(a):
        nbrhood = {b for b in G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) > rng + a.radius + b.radius:
                G.remove_edge(a, b)

    def finish(a, r):
        if len(G.A[a]) == 0 or r <= (epsilon / 4) * rng:
            absorb(a)
            for p in a:
                out[p] = nbrs[a]

    def update(a, ball):
        absorb(a)
        prune(a)
        finish(a, ball.radius)

    def init(ball):
        left, right = ball.left, ball.right
        nbrs[left] = nbrs.pop(ball, set())
        nbrs[right] = {b for b in nbrs[left]}

    def cleanup(a):
        finish(a, 0)

    out = defaultdict(set)
    nbrs = defaultdict(set)
    H = MaxHeap([A,B], key=lambda x:x.radius)
    G = ViabilityGraph(A,B)

    return G, H, init, update, cleanup, out

def all_range(A, B, rng, epsilon=0):
    G, H, init, update, cleanup, out = all_range_setup(A, B, rng, epsilon)
    dualtree_search(G, H, init, update, cleanup)
    return out

def all_range_analyze(A, B, rng, epsilon=0):
    G, H, init, update, cleanup, out = all_range_setup(A, B, rng, epsilon)
    for _ in dualtree_analysis(G, H, init, update, cleanup):
        yield G, out

if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = greedy_tree(MetricSpace([1,2,3,6,7,8,12], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    output = all_range(A, B, 2)
    for pt in output:
        print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')

    A = greedy_tree(MetricSpace([1,2,3,6,7,8], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    output = all_range(A, B, 5)
    for pt in output:
        print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')

    print("okay!")
