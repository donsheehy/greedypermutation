import unittest
from greedypermutation import Point, Cell, NeighborGraph
from metricspaces import MetricSpace

class L_inf(tuple):
    def dist(self, other):
        return max(abs(a-b) for a,b in zip(self, other))

class TestCell(unittest.TestCase):
    def testinit_with_center(self):
        M = MetricSpace([Point([2*i,2*i]) for i in range(100)])
        MetricCell = Cell(MetricSpace())
        C = MetricCell(Point([99,99]))
        for p in M:
            C.addpoint(p)
        self.assertEqual(len(C), 101)

    def testaddpoint(self):
        a,b,c = Point([1,2]), Point([2,3]), Point([3,4])
        MetricCell = Cell(MetricSpace())
        C = MetricCell(a)
        self.assertEqual(len(C), 1)
        C.addpoint(b)
        self.assertEqual(len(C), 2)
        C.addpoint(c)
        self.assertEqual(len(C), 3)
        self.assertEqual(C.points, {a,b,c})

    def testaddpoint_duplicatepoint(self):
        a,b = Point([1,2]), Point([2,3])
        MetricCell = Cell(MetricSpace())
        C = MetricCell(a)
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

    def testupdateradius_empty_cell(self):
        MetricCell = Cell(MetricSpace())
        C = MetricCell(Point([1,2,3]))
        C.updateradius()
        self.assertEqual(C.radius, 0)

    def testdist(self):
        MetricCell = Cell(MetricSpace())
        A = MetricCell(Point([2, 3]))
        self.assertEqual(A.dist(Point([7,3])), 5)
        self.assertEqual(A.dist(A.center), 0)
        self.assertEqual(A.dist(Point([7,15])), 13)

class TestNeighborGraph(unittest.TestCase):
    def testbasicusage(self):
        M = MetricSpace(((i,i) for i in range(100)), pointclass=Point)
        G = NeighborGraph(M)
        # root = next(G.vertices())
        # G.addcell(Point([100,99]), root)
        # self.assertEqual(len(G), 2)
        # for v in G.vertices():
        #     self.assertEqual(len(set(G.nbrs(v))), 1)

    def testrebalance(self):
        a, b = Point([-1]), Point([200])
        G = NeighborGraph(MetricSpace([a,b]))
        MetricCell = Cell(MetricSpace())
        A = MetricCell(a)
        B = MetricCell(b)
        for i in range(200):
            B.addpoint(Point([i]))
        self.assertEqual(len(A), 1)
        self.assertEqual(len(B), 201)
        G.rebalance(A, B)
        self.assertEqual(len(B), 101)
        self.assertEqual(len(A), 101)


    def testneighborsofneighborscondition(self):
        """ This somewhat long test was written to expose a bug where
        neighbors of the neighbor graph were not properly discovered.
        The construction highlights the need for the neighbor graph to be
        undirected.
        """
        a =  L_inf([0, 2, 21, 11, 22, 19])
        aa = L_inf([2, 0, 19, 9, 20, 17])
        b = L_inf([21, 19, 0, 10, 21, 18])
        bb = L_inf([11, 9, 10, 0, 11, 8])
        c = L_inf([22, 20 , 21, 11, 0, 3])
        cc = L_inf([ 19, 17, 18, 8, 3, 0])
        P = [a,aa,b,bb,c,cc]
        G = NeighborGraph(MetricSpace(P))
        self.assertEqual(len(G), 1)
        p = G.heap.findmax()
        self.assertEqual(p.center, a)
        self.assertEqual(p.pop(), c)
        G.addcell(c, p)
        self.assertEqual(len(G), 2)
        p = G.heap.findmax()
        self.assertEqual(p.pop(), b)
        G.addcell(b, p)
        V = {v.center : v for v in G.vertices()}
        self.assertEqual(set(V), {a,b,c})
        self.assertTrue(V[b] in G.nbrs(V[a]))
        self.assertTrue(V[a] in G.nbrs(V[b]))
        self.assertTrue(V[b] in G.nbrs(V[c]))
        self.assertTrue(V[c] in G.nbrs(V[b]))

        # Before adding aa.
        self.assertTrue(bb in V[b])
        self.assertEqual(V[a].pop(), aa)
        G.addcell(aa, V[a])
        V = {v.center:v for v in G.vertices()}
        # After adding aa.
        self.assertTrue(cc in V[c])
        self.assertTrue(bb in V[aa])
        self.assertTrue(bb.dist(cc) < bb.dist(aa))
        # That means that we should have an edge from c to aa.
        self.assertTrue(V[aa] in G.nbrs(V[c]))

    def testcellmass(self):
        P = [(i,i) for i in range(10)]
        M = MetricSpace(P, pointclass=L_inf)
        masslist = list(range(2,12))
        G = NeighborGraph(M, gettransportplan=True, mass=masslist)
        root_cell = next(iter(G._nbrs))
        self.assertEqual(G.cellmass(root_cell), 65)
        new_cell, update_plan = G.addcell((9,9), root_cell)
        self.assertEqual(G.cellmass(root_cell), 20)
        self.assertEqual(G.cellmass(new_cell), 45)
        print(update_plan)

if __name__ == '__main__':
    unittest.main()
