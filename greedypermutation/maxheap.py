# from .heap import Heap
from ds2.priorityqueue import PriorityQueue

class MaxHeap(PriorityQueue):
    def __init__(self, items = (), key = lambda x: x):
        PriorityQueue.__init__(self, key = lambda x: - key(x))
        for item in items:
            self.insert(item)

    # def compare(self, a, b):
    #     return self._items[a] > self._items[b]
    #
    # def reducekey(self, item):
    #     """
    #     Reduce the key of the given item.
    #     Note that the `MaxHeap` uses a separate dictionary to maintain find the
    #     index of `item`.
    #     This operation is different from the corresponding operation on a MinHeap.
    #     """
    #     index = self._itemmap[item]
    #     self._downheap(index)

    findmax = PriorityQueue.findmin
    removemax = PriorityQueue.removemin
