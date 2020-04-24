from ds2.priorityqueue import PriorityQueue

class MaxHeap(PriorityQueue):
    def __init__(self, items = (), key = lambda x: x):
        PriorityQueue.__init__(self, items, key = lambda x: - key(x))

    findmax = PriorityQueue.findmin
    removemax = PriorityQueue.removemin
