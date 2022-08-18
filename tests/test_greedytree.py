import unittest
from greedypermutation import GreedyTree
from greedypermutation.greedytree import Node, Bunch
from metricspaces import MetricSpace, R1

def ell_1(a, b):
    return abs(a-b)


class TestGreedyTree(unittest.TestCase):
    def testinit(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = GreedyTree(M, 0)
        # It should have 7 points
        self.assertEqual(len(T), len(M))
        # The point in the root node should be 0.
        self.assertEqual(T.root.point, 0)
        # The root has 3 children (100, 49, and 12)
        self.assertEqual(len(T.root.children), 3)
        # The first child is 100.
        onehundred = T.root.children[0]
        self.assertEqual(onehundred.point, 100)
        # The second child is 49.
        fortynine = T.root.children[1]
        self.assertEqual(fortynine.point, 49)
        # The third child is 12.
        twelve = T.root.children[2]
        self.assertEqual(twelve.point, 12)
        # Twelve has no children
        self.assertEqual(len(twelve.children), 0)
        # There are only two nodes in the subtree at onehundred.
        self.assertEqual(len(onehundred), 2)
        # The lone child of 100 is 81.
        self.assertEqual(onehundred.children[0].point, 81)

    def testinit_different_seed(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = GreedyTree(M, 49)
        # It should have 7 points
        self.assertEqual(len(T), len(M))
        # The point in the root node should be 0.
        self.assertEqual(T.root.point, 49)
        # The root has 4 children (100, 0, 25, and 12)
        self.assertEqual(len(T.root.children), 4)
        # The first child is 100.
        onehundred = T.root.children[0]
        self.assertEqual(onehundred.point, 100)
        # The second child is 49.
        zero = T.root.children[1]
        self.assertEqual(zero.point, 0)
        # The third child is 25.
        twentyfive = T.root.children[2]
        self.assertEqual(twentyfive.point, 25)
        # The fourth child is 60.
        sixty = T.root.children[3]
        self.assertEqual(sixty.point, 60)
        # Twenty-five has no children
        self.assertEqual(len(twentyfive.children), 0)
        # There are only two nodes in the subtree at onehundred.
        self.assertEqual(len(onehundred), 2)
        # The lone child of 100 is 81.
        self.assertEqual(onehundred.children[0].point, 81)
        # The lone child of 0 is 12.
        self.assertEqual(zero.children[0].point, 12)

    def testNN(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = GreedyTree(M)
        # self.P = [0, 100, 49, 25, 60, 12, 81]
        self.assertEqual(T.nn(11), 12)
        self.assertEqual(T.nn(5), 0)
        self.assertEqual(T.nn(51), 49)
        self.assertEqual(T.nn(75), 81)

    def testANN_eps_equals_zero(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = GreedyTree(M)
        self.assertEqual(T.ann(11), 12)
        self.assertEqual(T.ann(5), 0)
        self.assertEqual(T.ann(51), 49)
        self.assertEqual(T.ann(75), 81)

    def testnodeiter(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = GreedyTree(M, next(iter(M)))
        self.assertEqual(set(T.root), set(M))


if __name__ == '__main__':
    unittest.main()
