from greedypermutation.maxheap import MaxHeap
from greedypermutation.dualtrees.traversal import DualTreeSearch
from greedypermutation.dualtrees.viabilitygraph import ViabilityGraph
from collections import defaultdict


class AllRange(DualTreeSearch):
    def __init__(self, G_A, G_B, r, e=0):
        graph = ViabilityGraph(G_A, G_B)
        heap = MaxHeap([G_A,G_B], key=lambda x:x.radius)
        self.r = r
        self.e = e
        self.out = defaultdict(set)
        self.nbrs = defaultdict(set)
        super().__init__(graph, heap)

    def absorb(self, a):
        nbrhood = {b for b in self.G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) < self.r - a.radius - b.radius:
                self.G.remove_edge(a, b)
                self.nbrs[a].add(b)
    
    def prune(self, a):
        nbrhood = {b for b in self.G.A[a]}
        for b in nbrhood:
            if a.dist(b.center) > self.r + a.radius + b.radius:
                self.G.remove_edge(a, b)

    def finish(self, a, r):
        if len(self.G.A[a]) == 0 or r <= (self.e / 4) * self.r:
            self.absorb(a)
            for p in a:
                self.out[p] = self.nbrs[a]

    def update(self, node, ball):
        self.absorb(node)
        self.prune(node)
        self.finish(node, ball.radius)

    def init(self, ball):
        left, right = ball.left, ball.right
        self.nbrs[left] = self.nbrs.pop(ball, set())
        self.nbrs[right] = {b for b in self.nbrs[left]}

    def cleanup(self, node):
        self.finish(node, 0)

    def __call__(self):
        super().__call__()
        return self.out
    
    def __iter__(self):
        for _ in super().__iter__():
            yield self.G, self.out

if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = greedy_tree(MetricSpace([1,2,3,6,7,8,12], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    rng = AllRange(A, B, 2)
    output = rng()
    for pt in output:
        print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')

    A = greedy_tree(MetricSpace([1,2,3,6,7,8], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    rng = AllRange(A, B, 2)
    output = rng()
    for pt in output:
        print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')

    print("okay!")
