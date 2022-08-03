from ds2.priorityqueue import PriorityQueue

class KNNHeap(PriorityQueue):
    """
    The KNNHeap stores a collection of balls (max)heap ordered by an upper bound on
    their distance to a given query point.

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
        # Manually negating the priority as it comes out.
        return -(self._entries[0].priority)

    @property
    def top_weight(self):
        return len(self._entries[0].item)

    def remove(self, ball):
        """
        Remove the given ball and return its upper_bound.
        """
        # The following is a bit of a hack.
        L = self._entries
        index = self._itemmap[ball]
        # Manually negating the priority as it comes out.
        upper_bound = -(L[index].priority)
        L[index] = L[-1]
        L.pop()
        self.weight -= len(ball)
        return upper_bound

    def refine(self, ball):
        if not ball.isleaf():
            ub = self.remove(ball)
            right, left = ball.right, ball.left
            self.insert(left, min(ub, left.dist(self.query) + left.radius))
            self.insert(right, min(ub, right.dist(self.query) + right.radius))

    def insert(self, ball, upper_bound = None):
        if upper_bound is None:
            upper_bound = ball.dist(self.query) + ball.radius
        if self.weight < self.k or upper_bound < self.radius:
            # Manually negating priorities (for now).
            super().insert(ball, - upper_bound)
            self.weight += len(ball)
            self._tighten()

    def removemax(self):
        # The underlying priority queue is a min heap.
        return self.removemin()

    def _tighten(self):
        while self.weight - self.top_weight >= self.k:
            self.weight -= self.top_weight
            self.removemax()

    def __contains__(self, item):
        return item in self._itemmap

# class KNNHeap:
#     def __init__(self, k):
#         self.heap = MaxHeap(key = lambda x: x[1])
#         self.bunches = {}
#         self.k = k
#         self._len = 0
#
#     def __contains__(self, bunch):
#         return bunch in self.bunches
#
#     def insert(self, bunch, distance):
#         """
#         Insert a new bunch as long as it doesn't cause the heap to get too
#         large.  If the new bunch is closer than other bunches in the heap,
#         then some may be removed to make space.
#
#         The invariant maintained by insert is that if the bunches are sorted
#         by increasing upper bound distance to the query, then the heap contains
#         the minimum prefix that has at least k points.
#
#         The items inserted should be pairs.  This is important as we always
#         need the distance (i.e. the priority when we remove an item.)
#         """
#
#         if len(self) < self.k:
#             self.bunches[bunch] = distance
#             self.heap.insert((bunch, distance))
#         else:
#             top, current_radius = self.heap.findmax()
#             if distance < current_radius:
#                 if len(self) - len(top) + len(bunch) >= self.k:
#                     self.heap.removemax()
#                     del self.bunches[top]
#                 self.insert(bunch, distance)
#
#     def splitbunch(self, q, bunch):
#         """
#         Splits a bunch into two bunches using pop and tries to insert both
#         back into the heap.
#         """
#         b = bunch.pop()
#         b_radius = min(q.dist(b.point) + b.radius, self.bunches[bunch])
#
#         a = bunch
#         a_radius = min(q.dist(a.point) + a.radius, self.bunches[bunch])
#
#         del self.bunches[a]
#         self.insert(a, a_radius)
#         self.insert(b, b_radius)
#
#     def __len__(self):
#         return self._len
#
#     def __iter__(self):
#         return iter(self.heap)
