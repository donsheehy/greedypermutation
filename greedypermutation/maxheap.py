from .heap import Heap

class MaxHeap(Heap):
    def compare(self, a, b):
        return self._items[a] > self._items[b]

    def reducekey(self, item):
        """
        Reduce the key of the given item.
        Note that the `MaxHeap` uses a separate dictionary to maintain find the
        index of `item`.
        This operation is different from the corresponding operation on a MinHeap.
        """
        index = self._itemmap[item]
        self._downheap(index)

    findmax = Heap.peek
    removemax = Heap.pop
