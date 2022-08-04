from greedypermutation.knnheap import KNNHeap
from greedypermutation.balltree import Ball
import unittest


class TestKNNHeap(unittest.TestCase):
    def test_init(self):
        H = KNNHeap(3, 3)

    def testinsert_simple(self):
        H = KNNHeap(5, 2)


if __name__ == '__main__':
    unittest.main()
