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

if __name__ == '__main__':
    import unittest

    class DummyItem:
        def __init__(self, key):
            self.key = key

        def __gt__(self, other):
            return self.key > other.key

    class TestMaxHeap(unittest.TestCase):
        def testinit(self):
            H = MaxHeap()
            H = MaxHeap({1,2,3})
            H = MaxHeap([1,2,3])

        def testlen(self):
            self.assertEqual(len(MaxHeap()), 0)
            self.assertEqual(len(MaxHeap({1,2,3})), 3)
            self.assertEqual(len(MaxHeap(range(100))), 100)

        def testinsert(self):
            H = MaxHeap()
            H.insert(3)
            self.assertEqual(len(H), 1)
            H.insert(7)
            self.assertEqual(len(H), 2)
            self.assertEqual(H.findmax(), 7)
            H.insert(5)
            self.assertEqual(len(H), 3)
            self.assertEqual(H.findmax(), 7)

        def testfindmax(self):
            pass

        def testremovemax(self):
            H = MaxHeap([1,2,5,4,3])
            self.assertEqual(H.removemax(), 5)
            self.assertEqual(len(H), 4)
            self.assertEqual(H.removemax(), 4)
            self.assertEqual(len(H), 3)
            self.assertEqual(H.removemax(), 3)
            H.insert(9)
            H.insert(0)
            self.assertEqual(H.removemax(), 9)
            self.assertEqual(len(H), 3)
            self.assertEqual(H.removemax(), 2)

        def testheapify(self):
            H = MaxHeap([1,2,3])
            # Heapify is called on initialization.
            self.assertEqual(H.removemax(), 3)
            self.assertEqual(H.removemax(), 2)
            self.assertEqual(H.removemax(), 1)

        def testheapify_midfiedkeys(self):
            X = [DummyItem(i) for i in range(5)]
            H = MaxHeap(X)
            X[3].key = 100
            X[2].key = 50
            self.assertEqual(H.findmax(), X[4])
            H.heapify()
            self.assertEqual(H.removemax(), X[3])
            self.assertEqual(H.removemax(), X[2])
            self.assertEqual(H.removemax(), X[4])
            self.assertEqual(H.removemax(), X[1])
            self.assertEqual(H.removemax(), X[0])

        def testreducekey(self):
            A = [DummyItem(a) for a in [3,1,6,5,2,4]]
            H = MaxHeap(A)
            six = A[2]
            five = A[3]
            self.assertEqual(H.findmax(), six)
            six.key = 0 # Manually change the key.
            H.reducekey(six)
            self.assertEqual(H.findmax(), five)
            self.assertEqual(len(H), 6)

    unittest.main()
