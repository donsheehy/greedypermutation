from greedypermutation.maxheap import MaxHeap

class KNNHeap:
    def __init__(self, k):
        self.heap = MaxHeap(key = lambda x: x[1])
        self.bunches = {}
        self.k = k
        self._len = 0

    def __contains__(self, bunch):
        return bunch in self.bunches

    def insert(self, bunch, distance):
        """
        Insert a new bunch as long as it doesn't cause the heap to get too
        large.  If the new bunch is closer than other bunches in the heap,
        then some may be removed to make space.

        The invariant maintained by insert is that if the bunches are sorted
        by increasing upper bound distance to the query, then the heap contains
        the minimum prefix that has at least k points.

        The items inserted should be pairs.  This is important as we always
        need the distance (i.e. the priority when we remove an item.)
        """

        if len(self) < self.k:
            self.bunches[bunch] = distance
            self.heap.insert((bunch, distance))
        else:
            top, current_radius = self.heap.findmax()
            if distance < current_radius:
                if len(self) - len(top) + len(bunch) >= self.k:
                    self.heap.removemax()
                    del self.bunches[top]
                self.insert(bunch, distance)

    def splitbunch(self, q, bunch):
        """
        Splits a bunch into two bunches using pop and tries to insert both
        back into the heap.
        """
        b = bunch.pop()
        b_radius = min(q.dist(b.point) + b.radius, self.bunches[bunch])

        a = bunch
        a_radius = min(q.dist(a.point) + a.radius, self.bunches[bunch])

        del self.bunches[a]
        self.insert(a, a_radius)
        self.insert(b, b_radius)

    def __len__(self):
        return self._len

    def __iter__(self):
        return iter(self.heap)
