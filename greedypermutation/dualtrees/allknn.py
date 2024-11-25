from collections import defaultdict
from greedypermutation.maxheap import MaxHeap
from greedypermutation.knnheap import KNNHeap
from greedypermutation.dualtrees.traversal import DualTreeSearch
from greedypermutation.dualtrees.viabilitygraph import ViabilityGraph


class AllKNN(DualTreeSearch):
    def __init__(self, G_A, G_B, k, e=0):
        graph = ViabilityGraph(G_A, G_B)
        heap = MaxHeap([G_A,G_B], key=lambda x:x.radius)
        self.k = k
        self.knn_heaps = {G_A: KNNHeap(G_A.center, k)}
        self.knn_heaps[G_A].insert(G_B)
        self.out = defaultdict(set)
        self.e = e
        # self.nbrs = defaultdict(set)
        super().__init__(graph, heap)

    # def absorb(self, a):
    #     nbrhood = {b for b in G.A[a]}
    #     for b in nbrhood:
    #         if a.dist(b.center) < rng - a.radius - b.radius:
    #             G.remove_edge(a, b)
    #             self.nbrs[a].add(b)
    
    def update_candidates(self, a, ball):
        left, right = ball.left, ball.right
        if left in self.G.B:
            if ball in self.knn_heaps[a]:
                self.knn_heaps[a].refine(ball)
            else:
                self.knn_heaps[a].insert(left)
                self.knn_heaps[a].insert(right)
                self.knn_heaps[a].tighten()

    def prune(self, a):
        nbrhood = {b for b in self.G.A[a]}
        ub = self.knn_heaps[a].radius
        for b in nbrhood:
            if a.dist(b.center) > ub + 2*a.radius + b.radius:
                self.G.remove_edge(a, b)

    def finish(self, a):
        ub = self.knn_heaps[a].radius
        farthest = self.knn_heaps[a].findmax()
        lb = ub - 2*farthest.radius
        if 2*a.radius <= lb - ub/(1+self.e):
            # absorb(a)
            for p in a:
                self.out[p] = (ub + a.radius, farthest.center)

    def init(self, ball):
        left, right = ball.left, ball.right
        # self.nbrs[left] = nbrs.pop(ball, set())
        # self.nbrs[right] = {b for b in nbrs[left]}
        candidates = [b for b in self.knn_heaps.pop(ball, set())]
        self.knn_heaps[left] = KNNHeap(left.center, self.k)
        self.knn_heaps[right] = KNNHeap(right.center, self.k)
        for b in candidates:
            self.knn_heaps[left].insert(b)
            self.knn_heaps[right].insert(b)
        
    def update(self, node, ball):
        self.update_candidates(node, ball)
        # self.absorb(node)
        self.prune(node)
        self.finish(node)

    def cleanup(self, node):
        self.finish(node)

    def __call__(self):
        super().__call__()
        return self.out
    
    def __iter__(self):
        for _ in super().__iter__():
            yield self.G, self.out, self.knn_heaps


if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = list(range(2,15,3))
    B = list(range(1,20,4))
    k = 3

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], k)
    print([b for b in B])
    KNN = AllKNN(G_A, G_B, k)
    output = KNN()
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')

    A = [1,2,3,6,7,8]
    B = [1,2,3,6,7,9]
    k = 4

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], k)
    print([b for b in B])
    KNN = AllKNN(G_A, G_B, k)
    output = KNN()
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')

    print("okay!")
