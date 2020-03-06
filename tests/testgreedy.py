import unittest
from random import randrange
from greedypermutation import Point, MetricSpace, quadraticgreedy, clarksongreedy

class GreedyTests:
    def testgreedy(self):
        greedy = self.implementation.greedy
        P = [Point([i]) for i in range(3)]
        M = MetricSpace(P)
        gp = list(greedy(M, P[0]))
        self.assertEqual(gp, [P[0], P[2], P[1]])

    def testgreedy_exponential_example(self):
        greedy = self.implementation.greedy
        P = [Point([(-3)**i]) for i in range (100)]
        # print([str(p) for p in P])
        M = MetricSpace(P)
        gp = greedy(M, P[0])
        self.assertEqual(next(gp), P[0])
        self.assertEqual(next(gp), P[99])
        for i in range(98, 0, -1):
            self.assertEqual(next(gp), P[i])

    def testgreedytree_randomexample(self):
        greedytree = self.implementation.greedytree
        root = Point([0])
        P = MetricSpace([root] + [Point([x]) for x in [8,12, 100, 40, 70, 1, 72]])
        gp = greedytree(P, root)
        self.assertEqual(next(gp), (Point([0]), None))
        self.assertEqual(next(gp), (Point([100]), 0)) # radius = 100
        self.assertEqual(next(gp), (Point([40]), 0))
        self.assertEqual(next(gp), (Point([70]), 1))
        self.assertEqual(next(gp), (Point([12]), 0))
        self.assertEqual(next(gp), (Point([8]), 4))
        self.assertEqual(next(gp), (Point([72]), 3))

    def testgreedytree_bigexample(self):
        greedytree = self.implementation.greedytree
        n = 500
        coords = [(randrange(100), randrange(100), randrange(100)) for i in range(n)]
        P = [Point(c) for c in coords]
        M = MetricSpace(P)
        n = len(M) # we might get duplicate points.

        GP = list(greedytree(M, P[0]))
        radii = [p.dist(GP[i][0]) for p,i in GP if i is not None]
        # Check that the insertion radii are nonincreasing.
        for i in range(n-2):
            self.assertTrue(radii[i] >= radii[i+1], str([i, radii[i], radii[i+1]]))

class TestQuadraticGreedy(unittest.TestCase, GreedyTests):
    implementation = quadraticgreedy

class TestClarksonGreedy(unittest.TestCase, GreedyTests):
    implementation = clarksongreedy

if __name__ == '__main__':
    unittest.main()
