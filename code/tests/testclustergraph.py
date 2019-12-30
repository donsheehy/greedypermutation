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

    def testupdateradius_empty_cluster(self):
        C = Cluster(Point([1,2,3]))
        C.updateradius()
        self.assertEqual(C.radius, 0)


if __name__ == '__main__':
    unittest.main()
