import unittest
from metricspaces import MetricSpace, R1
from greedypermutation.balltree import Ball, greedy_tree


class TestBallTree(unittest.TestCase):
    def test_init_empty(self):
        BallTree = Ball(MetricSpace())
        B = BallTree(3)
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
        BallTree = Ball(MetricSpace())
        balltree = BallTree.tree(T)
        self.assertEqual(balltree.radius, 7)
        self.assertEqual(balltree.left.center, P[0])
        self.assertEqual(balltree.right.center, P[1])
        self.assertEqual(balltree.right.radius, 0)
        self.assertEqual(balltree.left.right.center, P[2])
        self.assertEqual(balltree.left.right.radius, 2)

    def test_greedytree(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)

        balltree = greedy_tree(M)
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

    def test_len(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)

        balltree = greedy_tree(M)
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
        self.assertEqual(len(balltree), 4)
        self.assertEqual(len(balltree.left), 2)
        self.assertEqual(len(balltree.right), 2)
        self.assertEqual(len(balltree.right.left), 1)
        self.assertEqual(len(balltree.right.right), 1)

    def test_iter(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)
        balltree = greedy_tree(M)
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
        self.assertEqual(set(M), set(balltree))
        self.assertEqual({M[0], M[1]}, set(balltree.left))
        self.assertEqual({M[2], M[3]}, set(balltree.right))
        self.assertEqual({M[2]}, set(balltree.right.right))

    def test_range(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)
        balltree = greedy_tree(M)
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
        self.assertEqual(set(M), set(balltree.range_search(R1(9), 8)))
        self.assertEqual({M[0], M[2]}, set(balltree.range_search(R1(12), 3)))

    def test_range_with_slack(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)
        balltree = greedy_tree(M)
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
        self.assertEqual(set(M), set(balltree.range_search(R1(9), 8, 0.5)))
        self.assertEqual({M[0], M[2], M[3]},
                         set(balltree.range_search(R1(13), 3, 3)))

    def test_range_count(self):
        M = MetricSpace([10, 4, 15, 17], pointclass=R1)
        balltree = greedy_tree(M)
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
        self.assertEqual(4, balltree.range_count(R1(9), 8))
        self.assertEqual(2, balltree.range_count(R1(12), 3))
        self.assertEqual(0, balltree.range_count(R1(6), 1))
        self.assertEqual(3, balltree.range_count(R1(12), 7))

    def test_knn(self):
        M = MetricSpace(range(100), pointclass=R1)
        balltree = greedy_tree(M)
        self.assertEqual(set(range(5, 10)), set(balltree.knn(5, R1(7))))
        self.assertEqual(set(range(18, 28)), set(balltree.knn(10, R1(22.2))))

    def test_knn_dist(self):
        M = MetricSpace(range(100), pointclass=R1)
        balltree = greedy_tree(M)
        self.assertEqual(2, balltree.knn_dist(5, R1(7)))
        self.assertEqual(3, balltree.knn_dist(6, R1(7)))
        self.assertEqual(4.5, balltree.knn_dist(10, R1(22.5)))


if __name__ == '__main__':
    unittest.main()
