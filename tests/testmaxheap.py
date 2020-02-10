import unittest
from context import greedypermutation
from greedypermutation import MaxHeap

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

if __name__ == '__main__':
    unittest.main()
