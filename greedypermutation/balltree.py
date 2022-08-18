from ds2.priorityqueue import PriorityQueue
from metricspaces import MetricSpace, metric_class
from greedypermutation.clarksongreedy import greedy
from greedypermutation.maxheap import MaxHeap
from greedypermutation.knnheap import KNNHeap


"""
This module contains an implementation of a ball tree.  It will eventually
replace the implementation of the greedy tree in `greedytree.py`.
This ball tree is a binary tree with the n leaves, one for each point.
In total, it has exactly 2n-1 nodes because every non-leaf node has two
children.
"""

def greedy_tree(M, seed=None):
    BallTree = Ball(M)
    gp = greedy(M, seed, pointtree=True)
    seed, _ = next(gp)
    root = BallTree(seed)
    leaf = {seed: root}
    for p, q in gp:
        node = leaf[q]
        leaf[q] = node.left = BallTree(q)
        leaf[p] = node.right = BallTree(p)
    root.update()
    return root



@metric_class
class Ball:
    """
    A Ball has a center, a radius, a numer of points that it contains, and a
    pair of children.  This means that each ball is the root of an entire ball
    tree.  There is no difference between a ball and a ball tree.
    """
    def __init__(self, point):
        self.center = point
        self._len = 1
        self.radius = 0
        self.left = None
        self.right = None

    def dist(self, other):
        return self.metric.dist(self.center, other)

    def isleaf(self):
        return self.left is None

    def intersects(self, center, radius):
        return self.dist(center) - self.radius <= radius

    def contained_in(self, center, radius):
        return self.dist(center) + self.radius <= radius

    def tree_greedy(M):
        gp = greedy(M, pointtree=True)
        return Ball.tree(gp)

    @classmethod
    def tree(cls, agp):
        """
        Initialize a binary greedy tree given an augmented
        greedy permutation `agp`.

        The augmented greedy permutation is given as an iterable of pairs
        of points `(p,q)` where `p` is a new point and `q` is its predecessor.
        """
        agp_iterator = iter(agp)
        seed, _ = next(agp_iterator)
        BallTree = Ball(cls.metric)
        root = BallTree(seed)
        leaf = {seed: root}
        for p, q in agp_iterator:
            node = leaf[q]
            leaf[q] = node.left = BallTree(q)
            leaf[p] = node.right = BallTree(p)
        root.update()
        return root

    def farthest(self, q):
        """Find the distance to the farthest point to `q`."""
        if self.isleaf():
            return self.dist(q)
        else:
            H = [self]
            best = 0
            while H:
                ball = H.pop()
                best = max(best, ball.dist(q))
                if not ball.isleaf() and \
                        ball.dist(q) + ball.radius > best:
                    H.append(ball.left)
                    H.append(ball.right)
            return best

    def update(self):
        """
        Recursively compute the `radius` and `len` of every ball in the tree
        rooted at self.
        """
        if self.isleaf():
            self.radius = 0
            self._len = 1
        else:
            self.left.update()
            self.right.update()
            self.radius = max(self.left.radius,
                              self.right.farthest(self.center))
            self._len = len(self.left) + len(self.right)

    def __len__(self):
        return self._len

    def __iter__(self):
        """
        Iterate over the points.

        Note that the current immplementation is simple, but not as efficient
        asymptotically as the non-recursive approach.  This is an issue with
        recursive iterators.
        """
        if self.isleaf():
            yield self.center
        else:
            yield from self.left
            yield from self.right

    def heap(self):
        """
        Construct and return a heap ordered by decreasing radius.
        The heap is initialized to contain `self`.
        """
        return PriorityQueue([self], key=lambda x: -x.radius)

    def nn(self, query):
        """
        Return the point in the ball tree that is closest to the query.
        """
        return self.ann(query, 1)

    def ann(self, query, approx=1):
        """
        Return the point in the ball tree that is closest to the query.
        """
        nbr, radius = self, self.dist(query)
        H = self.heap()
        for ball in H:
            current_dist = ball.dist(query)
            if current_dist < radius:
                nbr, radius = ball, current_dist
            if not ball.isleaf():
                if ball.left.intersects(query, radius / approx):
                    H.insert(ball.left)
                if ball.right.intersects(query, radius / approx):
                    H.insert(ball.right)
        return nbr.center

    def farthest_point(self, query):
        nbr, radius = self, self.dist(query)
        H = self.heap()
        for ball in H:
            current_dist = ball.dist(query)
            if current_dist > radius:
                nbr, radius = ball, current_dist
            if not ball.isleaf():
                if not ball.left.contained_in(query, radius):
                    H.insert(ball.left)
                if not ball.right.contained_in(query, radius):
                    H.insert(ball.right)
        return nbr.center

    def _range_search(self, center, radius, slack=0):
        """
        Iterate over the maximal balls contained in
        `ball(center, radius + slack)`.
        """
        H = self.heap()
        for ball in H:
            if ball.contained_in(center, radius + slack):
                yield ball
            else:
                if not ball.isleaf():
                    if ball.left.intersects(center, radius):
                        H.insert(ball.left)
                    if ball.right.intersects(center, radius):
                        H.insert(ball.right)

    def range_search(self, center, radius, slack=0):
        """
        Iterate over the points in `ball(center, radius)`.
        The output may include points contained in the slightly larger ball:
        `ball(center, radius + slack)`.
        """
        for ball in self._range_search(center, radius, slack):
            yield from ball

    def range_count(self, center, radius, slack=0):
        """
        Return the number of points in `ball(center, radius)`.
        """
        return sum(
            len(ball) for ball in self._range_search(center, radius, slack)
            )

    def approx_range_search(self, center, radius, approx):
        """
        Iterate over the points `ball(center, radius)`.
        The output may include points contained in the slightly larger ball:
        `ball(center, radius * approx)`.

        This is the multiplicative approximate range search.
        The standard range search allows for additive approximation.
        """
        yield from self.range_search(center, radius, (approx - 1) * radius)

    def approx_range_count(self, center, radius, approx):
        """
        Return the number of points in `ball(center, radius)`.
        The output may include points contained in the slightly larger ball:
        `ball(center, radius * approx)`.

        This is the multiplicative approximate range count.
        The standard range count allows for additive approximation.
        """
        return self.range_count(center, radius, (approx - 1) * radius)

    def _knn(self, k, query, approx):
        assert approx >= 1
        N = KNNHeap(query, k)
        N.insert(self, self.dist(query) + self.radius)
        H = self.heap()

        close_enough = (approx - 1) / 4

        for ball in H:
            if ball.radius <= close_enough * N.radius:
                # close_enough >= 0 implies that every leaf should reach here.
                # Make sure to put this ball back in H.
                H.insert(ball)
                return N, H
            if ball in N:
                N.refine(ball)
            else:
                N.insert(ball.left)
                N.insert(ball.right)
                N.tighten()
            if ball.left.intersects(query, N.radius):
                H.insert(ball.left)
            if ball.right.intersects(query, N.radius):
                H.insert(ball.right)

    def knn_dist(self, k, query, approx=1):
        N, _ = self._knn(k, query, approx)
        return N.radius

    def knn(self, k, query, approx=1):
        """
        Iterate over the k nearest points to the give query.

        For an approximation, the output will be a set of at least k points in
        the ball of radius `approx` times the distance to the true k nearest
        neighbors.
        """
        N, H = self._knn(k, query, approx)
        R = N.radius
        for ball in H:
            if ball.intersects(query,R):
                yield from ball
