class Heap:
    def __init__(self, items = None):
        self._items = list(items or [])
        self._itemmap = {item: i for (i,item) in enumerate(self._items)}
        self.heapify()

    def compare(self, a, b):
        return self._items[a] < self._items[b]

    def insert(self, item):
        self._items.append(item)
        self._upheap(len(self) - 1)

    def _parent(self, i):
        return (i - 1) // 2

    def _children(self, i):
        left = 2 * i + 1
        right_plus_one = min(2 * i + 3, len(self))
        return range(left, right_plus_one)


    def _swap(self, a, b):
        L = self._items
        self._itemmap[L[a]] = b
        self._itemmap[L[b]] = a
        L[a], L[b] = L[b], L[a]

    def _upheap(self, index):
        parent = self._parent(index)
        if index > 0 and self.compare(index, parent):
            self._swap(index, parent)
            self._upheap(parent)

    def peek(self):
        return self._items[0]

    def pop(self):
        item = self._items[0]
        self._swap(0, -1)
        del self._itemmap[item]
        self._items.pop()
        self._downheap(0)
        return item

    def _downheap(self, i):
        L = self._items
        children = self._children(i)
        if children:
            child = max(children, key = lambda x: L[x])
            if self.compare(child, i):
                self._swap(i, child)
                self._downheap(child)

    def heapify(self):
        n = len(self._items)
        for i in reversed(range(n)):
            self._downheap(i)


    def __len__(self):
        return len(self._items)
