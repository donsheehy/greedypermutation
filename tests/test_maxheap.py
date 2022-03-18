import unittest
from greedypermutation.maxheap import MaxHeap

class TestMaxHeap(unittest.TestCase):
    def testinit(self):
        H = MaxHeap()
        H = MaxHeap({1,2,3})
        H = MaxHeap([1,2,3])
        self.assertEqual(len(H), 3)

    def testfindmax(self):
        H = MaxHeap([1,2,5,4,3])
        self.assertEqual(H.findmax(), 5)

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

if __name__ == '__main__':
    unittest.main()
