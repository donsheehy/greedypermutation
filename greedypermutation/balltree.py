from ds2.priorityqueue import PriorityQueue
from metricspaces import MetricSpace
from greedypermutation.clarksongreedy import greedy

"""
This module contains an implementation of a ball tree.  It will eventually
replace the implementation of the greedy tree in `greedytree.py`.
This ball tree is a binary tree with the n leaves, one for each point.
In total, it has exactly 2n-1 nodes because every non-leaf node has two
children.
"""

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

    def isleaf(self):
        return self.left is None

    def tree_greedy(M):
        gp = greedy(M, pointtree=True)
        return Ball.tree(gp)

    def tree(agp):
        """
        Initialize a binary greedy tree given an augmented
        greedy permutation `agp`.

        The augmented greedy permutation is given as an iterable of pairs
        of points `(p,q)` where `p` is a new point and `q` is its predecessor.
        """
        agp_iterator = iter(agp)
        seed, _ = next(agp_iterator)
        root = Ball(seed)
        leaf = {seed:root}
        for p, q in agp_iterator:
            node = leaf[q]
            leaf[q] = node.left = Ball(q)
            leaf[p] = node.right = Ball(p)
        root.update()
        return root


    def farthest(self, q):
        """Find the distance to the farthest point to `q`."""
        if self.isleaf():
            return self.center.dist(q)
        else:
            viable = [self]
            best = 0
            while viable:
                ball = viable.pop()
                best = max(best, ball.center.dist(q))
                if not ball.isleaf() and \
                    ball.center.dist(q) + ball.radius > best:
                    viable.append(ball.left)
                    viable.append(ball.right)
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
            self._len = 1 + len(self.left) + len(self.right)

    def __len__(self):
        return self._len

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
        nbr = self.center
        nbr_dist = nbr.dist(query)
        H = self.heap()
        for ball in H:
            current_dist = ball.center.dist(query)
            if current_dist < nbr_dist:
                nbr = ball.center
                nbr_dist = current_dist
            left, right = ball.left, ball.right
            if left and left.center.dist(query) - left.radius < nbr_dist:
                H.insert(left)
            if right and right.center.dist(query) - right.radius < nbr_dist:
                H.insert(right)
        return nbr

    def knn(self, query, k):
        pass
