class MaxHeap:
    def __init__(self, items = None):
        self._items = list(items or [])
        self._itemmap = {item: i for (i,item) in enumerate(self._items)}
        self.heapify()

    def insert(self, item):
        self._items.append(item)
        self._upheap(len(self) - 1)

    def _parent(self, i):
        return (i - 1) // 2

    def _children(self, i):
        left, right = 2 * i + 1, 2 * i + 2
        return range(left, min(len(self._items), right + 1))

    def _swap(self, a, b):
        L = self._items
        self._itemmap[L[a]] = b
        self._itemmap[L[b]] = a
        L[a], L[b] = L[b], L[a]

    def _upheap(self, index):
        L = self._items
        parent = self._parent(index)
        if index > 0 and L[index] > L[parent]:
            self._swap(index,parent)
            self._upheap(parent)

    def findmax(self):
        return self._items[0]

    def removemax(self):
        L = self._items
        item = L[0]
        self._swap(0, len(L) - 1)
        del self._itemmap[item]
        L.pop()
        self._downheap(0)
        return item

    def _downheap(self, i):
        L = self._items
        children = self._children(i)
        if children:
            child = max(children, key = lambda x: L[x])
            if L[child] > L[i]:
                self._swap(i, child)
                self._downheap(child)

    def heapify(self):
        n = len(self._items)
        for i in reversed(range(n)):
            self._downheap(i)

    def reducekey(self, item):
        """
        Reduce the key of the given item.
        Note that the `MaxHeap` uses a separate dictionary to maintain find the
        index of `item`.
        """
        index = self._itemmap[item]
        self._downheap(index)

    def __len__(self):
        return len(self._items)
