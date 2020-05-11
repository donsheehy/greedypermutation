from collections import defaultdict
from greedypermutation.clarksongreedy import greedy
from greedypermutation.maxheap import MaxHeap

class Bunch:
    """
    A `Bunch` is a point with a `radius` and a `weight`.
    It stands in for a collection of points.

    The main way to access the points in a bunch is via the `pop` method.
    This returns a bunch and updates the current bunch.

    The main use is to be placed in a heap ordered by radius.
    By storing iterators, the child lists of the tree are not duplicated.
    """
    def __init__(self, node):
        self.point = node.point
        self.children = iter(node.children)
        self.weight = node.weight
        self.radii = iter(node.radii)
        self.radius = next(self.radii)

    def radius(self):
        return self.radius

    def isempty(self):
        return self.weight == 1

    def pop(self):
        try:
            output = next(self.children)
        except StopIteration:
            return None
        self.radius = next(self.radii)
        self.weight -= output.weight
        return Bunch(output)

    def __len__(self):
        return self.weight

class Node:
    """
    GreedyTree `Node`s store the follownig data.
    - a `point`: the location of the node.
    - a `weight`: the number of points in the subtree rooted at the node.
    - `children`: An ordered list of `Node`s.
    - `radii`: An ordered list of radii.  The ith entry is the radius of the
      subtree rooted at the Node with the first `i-1` children removed.
    """

    def __init__(self, point):
        self.point = point
        self.weight = 1
        self.children = []
        self.radii = [0]

    def update(self):
        """
        Update the weight and the radius list.
        """

        for c in reversed(self.children):
            c.update()
            self.weight = 1 + sum(c.weight for c in self.children)
            self.radii.append(max(self.radii[-1],
                                   c.farthest_descendant(self.point)
                                  ))
        self.radii.reverse()

    @property
    def radius(self):
        return self.radii[0]

    def farthest_descendant(self, point):
        """
        Return the largest distance from `point` to any point in the subtree
        rooted at `self`.

        Attempt to improve efficiency by pruning children that are too close.
        """
        farthest = self.point.dist(point)
        for c in self.children:
            if c.point.dist(point) + c.radius > farthest:
                farthest = max(farthest, c.farthest_descendant(point))
        return farthest

class GreedyTree:
    """
    The `GreedyTree` encodes a tree of points.
    If the points are ordered according to the greedy permutation, the child of
    a point is its nearest predecessor in the ordering.
    """

    def __init__(self, M, seed = None, scaling = float('inf')):
        """
        Initialize a new greedy tree on the input metric space `M`.
        """
        P = []
        self.ch = defaultdict(list)
        self.scaling = scaling
        alpha = 1 - (1/scaling)
        for p, i in greedy(M, seed, tree = True, alpha = alpha):
            newnode = Node(p)
            P.append(newnode)
            if i is not None:
                P[i].children.append(newnode)
        self.root = P[0]
        self.root.update()

    def heap(self):
        H = MaxHeap(key = Bunch.radius)
        H.insert(Bunch(self.root))
        return H

    def ann(self, q, eps = 0):
        """
        Return a (1+eps)-approximate nearest neighbor to q.
        """

        H = self.heap()
        nbr, q_to_nbr = self.root, q.dist(self.root.point)
        close_enough = eps / (1 + eps)

        for child in H:
            maxradius = child.radius

            # If the nearest neighbor could be a child of child.
            # if not child.isempty() and \
            if child.point.dist(q) < q_to_nbr + maxradius:
                p = child.pop()
                q_to_p = q.dist(p.point)
                # If p is the new nearest neighbors, update (nbr, q_to_nbr).
                if q_to_p < q_to_nbr:
                    nbr, q_to_nbr = p, q_to_p
                # If p is a sufficiently close ANN, return it.
                if maxradius < close_enough * q_to_p:
                    return nbr
                H.insert(p)
                H.insert(child) # Put the child back in the heap.
        return nbr.point

    def nn(self, q):
        """
        Return the nearest neighbor of q in the GreedyTree.
        """
        # return self.ann(q)
        H = self.heap()
        nbr, q_to_nbr = self.root, q.dist(self.root.point)

        for child in H:
            maxradius = child.radius      # update the maximum radius

            # If the nearest neighbor could be a child of child.
            # if not child.isempty() and \
            if child.point.dist(q) < q_to_nbr + maxradius:
                p = child.pop()
                q_to_p = q.dist(p.point)
                # If p is the new nearest neighbors, update (nbr, q_to_nbr).
                if q_to_p < q_to_nbr:
                    nbr, q_to_nbr = p, q_to_p
                H.insert(p)
                H.insert(child) # Put the child back in the heap.
        return nbr.point

    def _range(self, center, radius, slack = 0):
        """
        Produce a minimal collection of bunches that covers the range and is
        contained in the slack range.
        """
        H = self.heap()
        for child in H:
            maxradius = child.radius
            if child.point.dist(center) + maxradius <= radius + slack:
                yield child
            elif child.point.dist(center) <= radius + maxradius:
                p = child.pop()
                if p is not None:
                    H.insert(child)
                    H.insert(p)

    def rangecount(self, center, radius, slack = 0):
        """
        Count the points in the ball with the given `center` and `radius`.

        If the `slack` is nonzero then the count could include some points
        within distance `radius + slack` of the `center`.
        """
        bunches = self._range(center, radius, slack)
        return sum(bunch.weight for bunch in bunches)

    def range(self, center, radius, slack = 0):
        H = self.heap()

        for child in H:
            maxradius = child.radius
            if maxradius <= slack /2:
                H.insert(child)
                break
            if child.isempty():
                H.insert(child)
            elif child.point.dist(center) <= radius + maxradius:
                p = child.pop()
                H.insert(p)
                H.insert(child)

        return list((c.point, len(c))
                    for c in H
                    if c.point.dist(center) < radius + c.radius
                   )

    def __iter__(self):
        H = self.heap()
        yield self.root.point, None

        for child in H:
            if not child.isempty():
                q = child.pop()
                yield q.point, child.point
                H.insert(child)
                H.insert(q)


    def __str__(self):
        return str(self.ch)
