from greedypermutation.dualtrees.dualtreesearch import DualTreeSearch
from collections import defaultdict


class AllRange(DualTreeSearch):
    def __init__(self, G_A, G_B, r, e=0):
        """
        Initialize an all-range search.
        In addition to the greedy trees, the search radius and an approximation parameter are also part of the input.
        """
        super().__init__(G_A, G_B)
        self.r = r  # search radius
        self.e = e  # approximation parameter
        self.out = defaultdict(
            set
        )  # maps points to completed approximate range searches
        self.nbrs = defaultdict(
            set
        )  # maps nodes to partially completed searches for all points in the node

    def setup_children(self, ball):
        """
        This method initializes the partially finished searches of the children with those of the parent.
        """
        left, right = ball.left, ball.right
        self.nbrs[left] = self.nbrs.pop(ball, set())
        self.nbrs[right] = {b for b in self.nbrs[left]}

    def update(self, node, ball):
        """
        This method updates an affected vertex `node` when `ball` is replaced in the viability graph.
        """
        self.absorb(node)
        self.prune(node)
        self.finish(node, ball.radius)

    def cleanup(self, node):
        """
        This method finishes all remaining vertices in the graph when the heap only contains leaves.
        """
        self.finish(node, 0)

    def absorb(self, a):
        """
        This method iterates over the neighbors of `a`.
        If any of them should be in the output for all points in the subtree of `a`, then those edges are removed.
        Such edges are stored as partially completed searches for all points in `a`.
        """
        nbrhood = {b for b in self.G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) < self.r - a.radius - b.radius:
                self.G.remove_edge(a, b)
                self.nbrs[a].add(b)

    def prune(self, a):
        """
        This method prunes long edges adjacent to `a`.
        These neighbors are not viable with respect to any point in `a`.
        """
        nbrhood = {b for b in self.G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) > self.r + a.radius + b.radius:
                self.G.remove_edge(a, b)

    def finish(self, a, rmax):
        """
        This method checks if node `a` can be finished with respect to heap radius `rmax`.
        """
        if len(self.G.A[a]) == 0 or rmax <= (self.e / 4) * self.r:
            self.absorb(a)
            for p in a:
                self.out[p] = self.nbrs[a]

    def __call__(self):
        super().__call__()
        return self.out


def all_range_search(G_A, G_B, r, e=0):
    return AllRange(G_A, G_B, r, e)()


if __name__ == "__main__":
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = greedy_tree(MetricSpace([1, 2, 3, 6, 7, 8, 16], pointclass=R1))
    B = greedy_tree(
        MetricSpace([1, 2, 3, 6, 7, 9, 13, 14, 15, 16, 17, 18, 19, 20], pointclass=R1)
    )

    output = all_range_search(A, B, 6)
    for pt in output:
        print(f"{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}")

    A = greedy_tree(MetricSpace([1, 2, 3, 6, 7, 8], pointclass=R1))
    B = greedy_tree(MetricSpace([1, 2, 3, 6, 7, 9], pointclass=R1))

    output = all_range_search(A, B, 2)
    for pt in output:
        print(f"{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}")

    print("okay!")
