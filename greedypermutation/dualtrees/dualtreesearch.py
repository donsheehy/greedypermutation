from greedypermutation.maxheap import MaxHeap
from greedypermutation.dualtrees.viabilitygraph import ViabilityGraph


class DualTreeSearch:
    """
    A simple implementation of a generic dual-tree traversal using greedy trees.
    A dual-tree search algorithm can be built on top of this traversal.
    """

    def __init__(self, G_A, G_B):
        """
        The input is two greedy trees, one each for the two sets.
        The search maintains a viability graph and a max heap of nodes to traverse ordered by radii.
        """
        self.G = ViabilityGraph(G_A, G_B)
        self.H = MaxHeap([G_A, G_B], key=lambda x: x.radius)

    def setup_children(self, ball):
        """
        Method should initialize any attributes of the child vertex that should be inherited from the parent vertex.
        """
        pass

    def update(self, node, ball):
        """
        Method to update an affected vertex `node` when `ball` is the node at the top of the heap.
        """
        pass

    def cleanup(self, node):
        """
        Method to finish vertex `node` when all the remaining vertices are leaf nodes.
        """
        pass

    def __call__(self):
        for ball in self.H:
            if ball.isleaf():
                break
            self.iteration(ball)

        for a in self.G.A:
            self.cleanup(a)

    def __iter__(self):
        yield
        for ball in self.H:
            if ball.isleaf():
                break
            self.iteration(ball)
            yield

        for a in self.G.A:
            self.cleanup(a)

        yield

    def iteration(self, ball):
        """
        In an iteration of the traversal, the node at the top of the heap is replaced by its children in the viability graph.
        The new vertices are connected to the neighbors of the parent.
        """
        left, right = ball.left, ball.right

        if ball in self.G.A:
            self.G.add_vertices([left, right], self.G.A)
            self.setup_children(ball)
            for b in self.G.A.pop(ball):
                self.G.B[b].remove(ball)
                self.G.add_edges([(left, b), (right, b)])
            affected = {left, right}
        else:
            nbrhood = self.G.B.pop(ball)
            self.G.add_vertices([left, right], self.G.B)
            for a in nbrhood:
                self.G.A[a].remove(ball)
                self.G.add_edges([(a, left), (a, right)])
            affected = {a for a in nbrhood}

        for a in affected:
            self.update(a, ball)

        self.H.insert(left)
        self.H.insert(right)
