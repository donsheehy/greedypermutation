import unittest
from context import greedypermutation
from greedypermutation import Point, Cluster, ClusterGraph

class TestCluster(unittest.TestCase):
    def testinit_with_center(self):
        P = [Point([2*i,2*i]) for i in range(100)]
        C = Cluster(Point([99,99]))
        for p in P:
            C.addpoint(p)
        self.assertEqual(len(C), 101)

    def testaddpoint(self):
        a,b,c = Point([1,2]), Point([2,3]), Point([3,4])
        C = Cluster(a)
        self.assertEqual(len(C), 1)
        C.addpoint(b)
        self.assertEqual(len(C), 2)
        C.addpoint(c)
        self.assertEqual(len(C), 3)
        self.assertEqual(C.points, {a,b,c})

    def testaddpoint_duplicatepoint(self):
        a,b = Point([1,2]), Point([2,3])
        C = Cluster(a)
        self.assertEqual(len(C), 1)
        C.addpoint(b)
        self.assertEqual(len(C), 2)
        # Add b a second time.
        C.addpoint(b)
        self.assertEqual(len(C), 2)
        self.assertEqual(C.points, {a,b})
        # Add the center again.
        C.addpoint(a)
        self.assertEqual(len(C), 2)
        self.assertEqual(C.points, {a,b})

    def testupdateradius_empty_cluster(self):
        C = Cluster(Point([1,2,3]))
        C.updateradius()
        self.assertEqual(C.radius, 0)

    def testdist(self):
        A = Cluster(Point([2, 3]))
        self.assertEqual(A.dist(Point([7,3])), 5)
        self.assertEqual(A.dist(A.center), 0)
        self.assertEqual(A.dist(Point([7,15])), 13)

    def testrebalance(self):
        a, b = Point([-1]), Point([200])
        A = Cluster(a)
        B = Cluster(b)
        for i in range(200):
            B.addpoint(Point([i]))
        self.assertEqual(len(A), 1)
        self.assertEqual(len(B), 201)
        A.rebalance(B)
        self.assertEqual(len(B), 101)
        self.assertEqual(len(A), 101)

    def testpop(self):
        a,b,c,d = Point([0,0]), Point([100, 0]), Point([0,50]), Point([25,25])
        C = Cluster(a)
        C.addpoint(b)
        C.addpoint(c)
        C.addpoint(d)
        self.assertEqual(C.pop(), b)
        self.assertEqual(C.pop(), c)
        self.assertEqual(C.pop(), d)
        self.assertEqual(C.pop(), None)

class TestClusterGraph(unittest.TestCase):
    def testbasicusage(self):
        G = ClusterGraph([Point([i,i]) for i in range(100)])
        root = next(G.vertices())
        G.addcluster(Point([100,99]), root)
        self.assertEqual(len(G), 2)
        for v in G.vertices():
            self.assertEqual(len(set(G.nbrs(v))), 1)

if __name__ == '__main__':
    unittest.main()
