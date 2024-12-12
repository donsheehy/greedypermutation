class ViabilityGraph:
    """A bipartite graph with balls as vertices and edges
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
        for a, b in edges:
            self.add_edge(a, b)

    def add_edge(self, a, b):
        self.A.setdefault(a, set()).add(b)
        self.B.setdefault(b, set()).add(a)

    def add_vertices(self, vertices, part):
        for v in vertices:
            part[v] = set()

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
