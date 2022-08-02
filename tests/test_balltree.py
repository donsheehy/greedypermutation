import unittest
from metricspaces import MetricSpace, R1
from greedypermutation.balltree import Ball


class TestBallTree(unittest.TestCase):
    def test_init_empty(self):
        B = Ball(3)
        self.assertEqual(B.center, 3)
        self.assertEqual(B.radius, 0)
        self.assertEqual(len(B), 1)
        self.assertEqual(B.left, None)
        self.assertEqual(B.right, None)

    def test_tree(self):
        P = [R1(p) for p in [10, 5, 15, 17]]
        T = [(P[0], None), (P[1], P[0]), (P[2], P[0]), (P[3], P[2])]
        """
        The tree should have the following structure.
        10
            10
                10 (leaf)
                15
                    15 (leaf)
                    17 (leaf)
            5 (leaf)
        """
        balltree = Ball.tree(T)
        self.assertEqual(balltree.radius, 7)
        self.assertEqual(balltree.left.center, P[0])
        self.assertEqual(balltree.right.center, P[1])
        self.assertEqual(balltree.right.radius, 0)
        self.assertEqual(balltree.left.right.center, P[2])
        self.assertEqual(balltree.left.right.radius, 2)

    def test_greedytree(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)
        balltree = Ball.tree_greedy(M)
        """
        The tree should have the following structure.
        10
            10
                10 (leaf)
                 4 (leaf)
            17
                17 (leaf)
                15 (leaf)
        """
        self.assertEqual(balltree.radius, 7)
        self.assertEqual(balltree.left.center, M[0])
        self.assertEqual(balltree.right.center, M[3])
        self.assertEqual(balltree.right.radius, 2)
        self.assertEqual(balltree.left.radius, 6)
        self.assertEqual(balltree.left.left.radius, 0)
        self.assertEqual(balltree.left.right.center, M[1])
        self.assertEqual(balltree.left.right.radius, 0)


if __name__ == '__main__':
    unittest.main()
