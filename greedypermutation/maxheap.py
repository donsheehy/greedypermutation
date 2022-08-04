from ds2.priorityqueue import PriorityQueue


class MaxHeap(PriorityQueue):
    def __init__(self, items=(), key=lambda x: x):
        super().__init__(items, key=lambda x: -key(x))

    def insert(self, item, priority=None):
        if priority is not None:
            priority = -priority
        super().insert(item, priority)

    def priority(self, item):
        return - self._entries[self._itemmap[item]].priority

    findmax = PriorityQueue.findmin
    removemax = PriorityQueue.removemin
