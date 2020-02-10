from .heap import Heap

class MinHeap(Heap):
    def compare(self, a, b):
        return self._items[a] < self._items[b]

    def reducekey(self, item):
        """
        Reduce the key of the given item.
        Note that the `MinHeap` uses a separate dictionary to maintain find the
        index of `item`.
        This operation is different from the corresponding operation on a MaxHeap.
        """
        index = self._itemmap[item]
        self._upheap(index)

    findmin = Heap.peek
    removemin = Heap.pop
