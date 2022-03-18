from greedypermutation.knnheap import KNNHeap
from greedypermutation.greedytree import Bunch
import unittest


class TestKNNHeap(unittest.TestCase):
    def setup(self):
        print("running a test")

    def testinit(self):
        H = KNNHeap(3)

    def testinsert_simple(self):
        H = KNNHeap(5)

        # B = Bunch()
        # H.insert()

if __name__ == '__main__':
    unittest.main()
