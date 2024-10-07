import logging
from ds2.priorityqueue import PriorityQueue
from metricspaces import metric_class
from greedypermutation.clarksongreedy import greedy
from greedypermutation.maxheap import MaxHeap

logging.basicConfig(level=logging.NOTSET)


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
                if not ball.isleaf() and ball.dist(q) + ball.radius > best:
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
            # SID: To compute approximate node radii, we need scale and locally greedy parameters
            self.radius = max(self.left.radius, self.right.farthest(self.center))
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

    def _str(self, s="", tabs=0):
        if self is not None:
            s += tabs * "|\t" + str(self.center) + "\n"
            if not self.isleaf():
                s = self.left._str(s, tabs=tabs + 1)
                s = self.right._str(s, tabs=tabs + 1)
            s += tabs * "|\t" + "\n"
        return s

    def __str__(self):
        return self._str()
