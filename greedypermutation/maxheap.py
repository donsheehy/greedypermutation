# from .heap import Heap
from ds2.priorityqueue import PriorityQueue

class MaxHeap(PriorityQueue):
    def __init__(self, items = (), key = lambda x: x):
        PriorityQueue.__init__(self, key = lambda x: - key(x))
        for item in items:
            self.insert(item)

    findmax = PriorityQueue.findmin
    removemax = PriorityQueue.removemin
