import unittest
from context import greedypermutation
from greedypermutation import Point, MetricSpace, quadraticgreedy

greedy = None

class _:
    class TestGreedy(unittest.TestCase):
        def testgreedy(self):
            greedy = self.implementation.greedy
            P = [Point([i]) for i in range(3)]
            M = MetricSpace(P)
            gp = list(greedy(M))
            self.assertEqual(gp, [P[0], P[2], P[1]])

        def testgreedy_exponential_example(self):
            greedy = self.implementation.greedy
            P = [Point([(-3)**i]) for i in range (100)]
            # print([str(p) for p in P])
            M = MetricSpace(P)
            gp = greedy(M)
            self.assertEqual(next(gp), P[0])
            self.assertEqual(next(gp), P[99])
            for i in range(98, 0, -1):
                self.assertEqual(next(gp), P[i])

class TestQuadraticGreedy(_.TestGreedy):
    implementation = quadraticgreedy

# class TestClarksonGreedy(_.TestGreedy):
#     implementation = clarksongreedy

if __name__ == '__main__':
    unittest.main()
