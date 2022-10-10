from greedypermutation.maxheap import MaxHeap

class NNBallGraph:
    """ A bipartite graph with balls as vertices and edges
    corresponding to pairs of balls that can contain
    an edge of the nearest neighbor graph.

    It is always initialized with a pair of balls.
    """

    def __init__(self, a, b):
        self.B = {b: {a}}
        self.A = {a: {b}}
        self.mindist = {}
        self.update_mindist(a)

    def update_mindist(self, a):
        self.mindist[a] = min(a.dist(b.center) for b in self.A[a])

    def lower_bound(self, a):
        return min(a.dist(b.center) - b.radius for b in self.A[a])

    def add_edges(self, edges):
        for a,b in edges:
            self.add_edge(a,b)

    def add_edge(self, a, b):
        self.A.setdefault(a, set()).add(b)
        self.B.setdefault(b, set()).add(a)

    def prune(self, a):
        self.update_mindist(a)
        threshold = self.mindist[a] + 2 * a.radius
        for b in [b for b in self.A[a] if a.dist(b.center) - b.radius > threshold]:
            self.remove_edge(a,b)

    def remove_edge(self, a, b):
        self.B[b].remove(a)
        self.A[a].remove(b)

    def remove(self, ball):
        """
        Remove a ball from the graph and return its set of neighbors.
        """
        if ball in self.A:
            for b in self.A[ball]:
                self.B[b].remove(ball)
            return self.A.pop(ball)
        if ball in self.B:
            for a in self.B[ball]:
                self.A[a].remove(ball)
            return self.B.pop(ball)


def dist_H(A, B, epsilon=0):
    H = MaxHeap([A,B], key=lambda x:x.radius)
    G = NNBallGraph(A,B)
    LB = 0
    lb = {}

    for ball in H:
        if ball.radius <= (epsilon / 2) * LB:
            return LB

        L, R = ball.left, ball.right

        if ball in G.A:
            for b in G.A.pop(ball):
                G.B[b].remove(ball)
                G.add_edges([(L, b), (R, b)])
            lb[L], lb[R] = G.lower_bound(L), G.lower_bound(R)
            LB = max(LB, lb[L], lb[R])
            G.prune(L), G.prune(R)

        if ball in G.B:
            for a in G.B.pop(ball):
                G.A[a].remove(ball)
                G.add_edges([(a, L), (a, R)])
                lb[a] = G.lower_bound(a)
                LB = max(LB, lb[a])
                G.prune(a)

        H.insert(L)
        H.insert(R)

if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = greedy_tree(MetricSpace([1,2,3,6,7,8,12], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    assert(dist_H(A, B) == 3)

    A = greedy_tree(MetricSpace([1,2,3,6,7,8], pointclass = R1))
    B = greedy_tree(MetricSpace([1,2,3,6,7,9], pointclass = R1))

    assert(dist_H(A, B) == 1)
    print("okay!")
