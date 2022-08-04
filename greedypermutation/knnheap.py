from greedypermutation.maxheap import MaxHeap


class KNNHeap(MaxHeap):
    """
    The KNNHeap stores a collection of balls (max)heap ordered by an upper
    bound on their distance to a given query point.

    If `N` is a the KNNHeap and `N'` is the same heap after removing the max
    ball, then `N'.weight < k <= N.weight`.
    """
    def __init__(self, query, k):
        super().__init__()
        self.query = query
        self.k = k
        self.weight = 0

    @property
    def radius(self):
        return self.priority(self.findmax())

    @property
    def top_weight(self):
        return len(self.findmax())

    def remove(self, ball):
        """
        Remove the given ball and return its upper_bound.
        """
        upper_bound = self.priority(ball)
        super().remove(ball)
        self.weight -= len(ball)
        return upper_bound

    def refine(self, ball):
        if not ball.isleaf():
            ub = self.remove(ball)
            right, left = ball.right, ball.left
            self.insert(left, min(ub, left.dist(self.query) + left.radius))
            self.insert(right, min(ub, right.dist(self.query) + right.radius))
        self.tighten()

    def insert(self, ball, upper_bound=None):
        if upper_bound is None:
            upper_bound = ball.dist(self.query) + ball.radius
        super().insert(ball, upper_bound)
        self.weight += len(ball)

    def tighten(self):
        while self.weight - self.top_weight >= self.k:
            self.weight -= self.top_weight
            self.removemax()

    def __contains__(self, item):
        return item in self._itemmap
