import unittest
from greedypermutation import greedy_tree
from metricspaces import MetricSpace

def ell_1(a, b):
    return abs(a-b)


class TestGreedyTree(unittest.TestCase):
    def testinit(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = greedy_tree(M, 0)
        # It should have 7 points
        self.assertEqual(len(T), len(M))
        # The point in the root node should be 0.
        self.assertEqual(T.center, 0)
        # The root has 3 children (100, 49, and 12)
        # self.assertEqual(len(T), 3)
        # The first child is 100.
        onehundred = T.right
        self.assertEqual(onehundred.center, 100)
        # The second child is 49.
        fortynine = T.left.right
        self.assertEqual(fortynine.center, 49)
        # The third child is 12.
        twelve = T.left.left.right
        self.assertEqual(twelve.center, 12)
        # Twelve is a leaf node
        self.assertEqual(len(twelve), 1)
        # There are only two nodes in the subtree at onehundred.
        self.assertEqual(len(onehundred), 2)
        # There are three nodes in the subtree at fortynine
        self.assertEqual(len(fortynine), 3)
        # The lone child of 100 is 81.
        self.assertEqual(onehundred.right.center, 81)

    def testinit_different_seed(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = greedy_tree(M, 49)
        # It should have 7 points
        self.assertEqual(len(T), len(M))
        # The point in the root node should be 0.
        self.assertEqual(T.center, 49)
        # The root has 4 children (100, 0, 25, and 12)
        # self.assertEqual(len(T.root.children), 4)
        # The first child is 100.
        onehundred = T.right
        self.assertEqual(onehundred.center, 100)
        # The second child is 0.
        zero = T.left.right
        self.assertEqual(zero.center, 0)
        # The third child is 25.
        twentyfive = T.left.left.right
        self.assertEqual(twentyfive.center, 25)
        # The fourth child is 60.
        sixty = T.left.left.left.right
        self.assertEqual(sixty.center, 60)
        # Twenty-five has no children
        self.assertEqual(len(twentyfive), 1)
        # There are only two nodes in the subtree at onehundred.
        self.assertEqual(len(onehundred), 2)
        # The lone child of 100 is 81.
        self.assertEqual(onehundred.right.center, 81)
        # The lone child of 0 is 12.
        self.assertEqual(zero.right.center, 12)

    def testNN(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = greedy_tree(M)
        # self.P = [0, 100, 49, 25, 60, 12, 81]
        self.assertEqual(T.nn(11), 12)
        self.assertEqual(T.nn(5), 0)
        self.assertEqual(T.nn(51), 49)
        self.assertEqual(T.nn(75), 81)

    def testANN_eps_equals_zero(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = greedy_tree(M)
        self.assertEqual(T.ann(11), 12)
        self.assertEqual(T.ann(5), 0)
        self.assertEqual(T.ann(51), 49)
        self.assertEqual(T.ann(75), 81)

    def testnodeiter(self):
        M = MetricSpace([0, 100, 49, 25, 60, 12, 81], dist=ell_1)
        T = greedy_tree(M, next(iter(M)))
        self.assertEqual(set(T), set(M))


if __name__ == '__main__':
    unittest.main()
