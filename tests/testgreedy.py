import unittest
from random import randrange, seed
from collections import defaultdict
from greedypermutation import (Point,
                               quadraticgreedy,
                               clarksongreedy,
                               )
from metricspaces import MetricSpace

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
        greedy = self.implementation.greedy
        root = Point([0])
        P = MetricSpace([root] + [Point([x]) for x in [8,12, 100, 40, 70, 1, 72]])
        gp = greedy(P, root, tree = True)
        self.assertEqual(next(gp), (Point([0]), None))
        self.assertEqual(next(gp), (Point([100]), 0)) # radius = 100
        self.assertEqual(next(gp), (Point([40]), 0))
        self.assertEqual(next(gp), (Point([70]), 1))
        self.assertEqual(next(gp), (Point([12]), 0))
        self.assertEqual(next(gp), (Point([8]), 4))
        self.assertEqual(next(gp), (Point([72]), 3))

    def testgreedytree_transportplan(self):
        """
        This test determines that greedy() computes the correct transportation plan
        """
        greedy = self.implementation.greedy
        root = Point([0])
        P = MetricSpace([root] + [Point([x]) for x in [9,3,5,18]])
        #gp = greedy(P, root, tree=False, gettransportplan = True)
        gp = greedy(P, root, tree=False, gettransportplan = True)

        # A case-wise assertion was needed because the way clarksongreedy.greedy works,
        # it looks into all neighbors which might have been changed when a new cell was 
        # created. So the transportation plan has entries in the dictionary with 0 mass 
        # moved. On the other hand quadraticgreedy.greedy stores points in the  
        # transportation plan only if their reverse nearest neighbor changed. 
        # So there are no 0 value keys here.
        if self.implementation == clarksongreedy:
            self.assertEqual(next(gp), (Point([0]), {Point([0]): 5}))
            self.assertEqual(next(gp), (Point([18]), {Point([0]): -1, Point([18]): 1}))
            self.assertEqual(next(gp), (Point([9]), {Point([9]):2, Point([0]): -2, Point([18]): 0}))
            self.assertEqual(next(gp), (Point([5]), {Point([9]):-1, Point([0]): -1, Point([5]): 2}))
            self.assertEqual(next(gp), (Point([3]), {Point([9]):0, Point([3]): 1, Point([5]): -1}))
        else:
            self.assertEqual(next(gp), (Point([0]), {Point([0]): 5}))
            self.assertEqual(next(gp), (Point([18]), {Point([0]): -1, Point([18]): 1}))
            self.assertEqual(next(gp), (Point([9]), {Point([9]):2, Point([0]): -2}))
            self.assertEqual(next(gp), (Point([5]), {Point([9]):-1, Point([0]): -1, Point([5]): 2}))
            self.assertEqual(next(gp), (Point([3]), {Point([3]): 1, Point([5]): -1}))

    def testgreedytree_transportplan_mass(self):
        """
        This test determines that greedy() computes the correct transportation plan
        """
        greedy = self.implementation.greedy
        root = Point([0])
        P = MetricSpace([root] + [Point([x]) for x in [9,3,5,18]])
        #gp = greedy(P, root, tree=False, gettransportplan = True)
        gp = greedy(P, root, tree=False, gettransportplan = True, mass = [2,2,2,2,2])

        # A case-wise assertion was needed because the way clarksongreedy.greedy works,
        # it looks into all neighbors which might have been changed when a new cell was 
        # created. So the transportation plan has entries in the dictionary with 0 mass 
        # moved. On the other hand quadraticgreedy.greedy stores points in the  
        # transportation plan only if their reverse nearest neighbor changed. 
        # So there are no 0 value keys here.
        if self.implementation == clarksongreedy:
            self.assertEqual(next(gp), (Point([0]), {Point([0]): 10}))
            self.assertEqual(next(gp), (Point([18]), {Point([0]): -2, Point([18]): 2}))
            self.assertEqual(next(gp), (Point([9]), {Point([9]):4, Point([0]): -4, Point([18]): 0}))
            self.assertEqual(next(gp), (Point([5]), {Point([9]):-2, Point([0]): -2, Point([5]): 4}))
            self.assertEqual(next(gp), (Point([3]), {Point([9]):0, Point([3]): 2, Point([5]): -2}))
        else:
            self.assertEqual(next(gp), (Point([0]), {Point([0]): 10}))
            self.assertEqual(next(gp), (Point([18]), {Point([0]): -2, Point([18]): 2}))
            self.assertEqual(next(gp), (Point([9]), {Point([9]):4, Point([0]): -4}))
            self.assertEqual(next(gp), (Point([5]), {Point([9]):-2, Point([0]): -2, Point([5]): 4}))
            self.assertEqual(next(gp), (Point([3]), {Point([3]): 2, Point([5]): -2}))


    def testgreedytree_bigexample(self):
        greedy = self.implementation.greedy
        n = 600
        coords = set()
        while len(coords) < n:
            coords.add((randrange(100), randrange(100), randrange(100)))
        P = [Point(c) for c in coords]
        M = MetricSpace(P)

        GP = list(greedy(M, P[0], tree = True))
        radii = [p.dist(GP[i][0]) for p,i in GP if i is not None]
        # Check that the insertion radii are nonincreasing.
        for i in range(n-2):
            self.assertTrue(radii[i] >= radii[i+1], str([i, radii[i], radii[i+1]]))

    def testgreedytree_example2(self):
        greedy = self.implementation.greedy
        P = [Point([c]) for c in [0, 100, 49, 25, 60, 12, 81]]
        M = MetricSpace(P)
        root = P[0]
        gt = list(greedy(M, root, tree = True))
        gp = [p for p, i in gt]
        ch = defaultdict(list)
        for p, i in greedy(M, root, tree = True):
            if i is not None:
                ch[gp[i]].append(p)
        self.assertEqual(gp, [P[i] for i in [0, 1, 2, 3, 6, 5, 4]])

    def testgreedytree_example3(self):
        greedy = self.implementation.greedy
        P = [Point([c]) for c in [0, 1, 3, 5, 20, 30]]
        M = MetricSpace(P)
        gt = list(greedy(M, P[0], tree = True))
        gp = [p for p, i in gt]
        ch = defaultdict(set)
        for p, i in gt:
            if i is not None:
                ch[gp[i]].add(p)

        self.assertEqual(gp, [P[0], P[5], P[4], P[3], P[2], P[1]])
        self.assertEqual(ch[P[0]], {P[5], P[3], P[1]})
        self.assertEqual(ch[P[1]], set())
        self.assertEqual(ch[P[2]], set())
        self.assertEqual(ch[P[3]], {P[2]})
        self.assertEqual(ch[P[4]], set())
        self.assertEqual(ch[P[5]], {P[4]})

def _test(impl):
    class GreedyTestCase(unittest.TestCase, GreedyTests):
        implementation = impl
    return GreedyTestCase


TestQuadraticGreedy = _test(quadraticgreedy)
TestClarksonGreedy = _test(clarksongreedy)

if __name__ == '__main__':
    unittest.main()
