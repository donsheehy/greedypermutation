from collections import defaultdict
from greedypermutation.knnheap import KNNHeap
from greedypermutation.dualtrees.dualtreesearch import DualTreeSearch


class AllKNN(DualTreeSearch):
    def __init__(self, G_A, G_B, k, e=0):
        """
        Initialize an all-KNN search.
        In addition to the greedy trees, a parameter `k` and an approximation parameter are also part of the input.
        """
        super().__init__(G_A, G_B)
        self.k = k
        self.e = e
        self.out = defaultdict(set)  # maps points to their approximate kNNs
        self.knn_heaps = {
            G_A: KNNHeap(G_A.center, k)
        }  # maps vertices to their candidate heaps.
        self.knn_heaps[G_A].insert(G_B)
        self.nbrs = defaultdict(set)  # maps vertices to partially completed searches

    def setup_children(self, ball):
        """
        This method initializes the partially finished searches of the children with those of the parent.
        """
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
        """
        This method updates an affected vertex `node` when `ball` is replaced in the viability graph.
        """
        self.update_candidates(node, ball)
        # self.absorb(node)
        self.prune(node)
        self.finish(node, ball.radius)

    def cleanup(self, node):
        """
        This method finishes all remaining vertices in the graph when the heap only contains leaves.
        """
        self.finish(node, 0)

    # def absorb(self, a):
    #     nbrhood = {b for b in G.A[a]}
    #     for b in nbrhood:
    #         if a.dist(b.center) < rng - a.radius - b.radius:
    #             G.remove_edge(a, b)
    #             self.nbrs[a].add(b)

    def update_candidates(self, a, ball):
        """
        For affected vertex `a` update its candidate set with the children of `ball`.
        """
        left, right = ball.left, ball.right
        if left in self.G.B:
            if ball in self.knn_heaps[a]:
                self.knn_heaps[a].refine(ball)
            else:
                self.knn_heaps[a].insert(left)
                self.knn_heaps[a].insert(right)
                self.knn_heaps[a].tighten()

    def prune(self, a):
        """
        This method prunes long edges adjacent to `a`.
        These neighbors are not viable with respect to any point in `a`.
        """
        nbrhood = {b for b in self.G.A[a]}
        ub = self.knn_heaps[a].radius
        for b in nbrhood:
            if a.dist(b.center) > ub + 2 * a.radius + b.radius:
                self.G.remove_edge(a, b)

    def finish(self, a, rmax=0):
        """
        This method checks if node `a` can be finished with respect to heap radius `rmax`.
        """
        ub = self.knn_heaps[a].radius
        lb = ub - 2 * rmax
        farthest = self.knn_heaps[a].findmax()
        if 2 * a.radius <= lb - ub / (1 + self.e):
            # absorb(a)
            for p in a:
                self.out[p] = (ub + a.radius, farthest.center)

    def __call__(self):
        super().__call__()
        return self.out


def all_knn_search(G_A, G_B, k, e=0):
    return AllKNN(G_A, G_B, k, e)()


if __name__ == "__main__":
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = list(range(2, 15, 3))
    B = list(range(1, 20, 4))
    k = 3

    G_A = greedy_tree(MetricSpace(A, pointclass=R1))
    G_B = greedy_tree(MetricSpace(B, pointclass=R1))

    print([a for a in A], k)
    print([b for b in B])
    output = all_knn_search(G_A, G_B, k)
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f"{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}")

    A = [1, 2, 3, 6, 7, 8]
    B = [1, 2, 3, 6, 7, 9]
    k = 4

    G_A = greedy_tree(MetricSpace(A, pointclass=R1))
    G_B = greedy_tree(MetricSpace(B, pointclass=R1))

    print([a for a in A], k)
    print([b for b in B])
    output = all_knn_search(G_A, G_B, k)
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f"{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}")

    print("okay!")
