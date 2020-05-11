from greedypermutation import Point, MetricSpace, GreedyTree
import unittest


class TestGreedyTree(unittest.TestCase):
    def setUp(self):
        self.P = [Point([c]) for c in [0, 100, 49, 25, 60, 12, 81]]
        self.M = MetricSpace(self.P)

    def testinit(self):
        P = self.P
        T = GreedyTree(self.M, P[0])
        # self.assertEqual(len(T.ch), 3)
        # self.assertEqual(T.root, P[0])
        # self.assertEqual(T.ch[P[0]], [P[1], P[2], P[5]])
        # self.assertEqual(T.ch[P[1]], [P[6]])
        # self.assertEqual(T.ch[P[2]], [P[3], P[4]])

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

    def testANN_big_example(self):
        pass


if __name__ == '__main__':
    unittest.main()
