from greedypermutation import GreedyTree
from greedypermutation.greedytree import Node, Bunch
from metricspaces import MetricSpace, NumpyPoint as Point
import unittest


class TestGreedyTree(unittest.TestCase):
    def setUp(self):
        self.P = [Point([c]) for c in [0, 100, 49, 25, 60, 12, 81]]
        self.M = MetricSpace(self.P)

    def testinit(self):
        P = self.P
        T = GreedyTree(self.M, P[0])
        # It should have 7 points
        self.assertEqual(len(T), len(self.P))
        # It should have a root that is a node.
        self.assertTrue(isinstance(T.root, Node))
        # The point in the root node should be P[0].
        self.assertEqual(T.root.point, P[0])
        # The root has 3 children (100, 49, and 12)
        self.assertEqual(len(T.root.children), 3)
        # The first child is 100.
        onehundred = T.root.children[0]
        self.assertEqual(onehundred.point, P[1])
        # The second child is 49.
        fortynine = T.root.children[1]
        self.assertEqual(fortynine.point, P[2])
        # The third child is 12.
        twelve = T.root.children[2]
        self.assertEqual(twelve.point, P[5])
        # Twelve has no children
        self.assertEqual(len(twelve.children), 0)
        # There are only two nodes in the subtree at onehundred.
        self.assertEqual(len(onehundred), 2)
        # The lone child of 100 is 81.
        self.assertEqual(onehundred.children[0].point, P[6])

    def testNN(self):
        P = self.P
        T = GreedyTree(self.M)
        self.assertEqual(T.nn(Point([11])), P[5])
        self.assertEqual(T.nn(Point([5])), P[0])
        self.assertEqual(T.nn(Point([51])), P[2])
        self.assertEqual(T.nn(Point([75])), P[6])

    def testANN_eps_equals_zero(self):
        P = self.P
        T = GreedyTree(self.M)
        self.assertEqual(T.ann(Point([11])), P[5])
        self.assertEqual(T.ann(Point([5])), P[0])
        self.assertEqual(T.ann(Point([51])), P[2])
        self.assertEqual(T.ann(Point([75])), P[6])

    def testnodeiter(self):
        T = GreedyTree(self.M, next(iter(self.M)))
        self.assertEqual(set(T.root), set(self.M))


if __name__ == '__main__':
    unittest.main()
