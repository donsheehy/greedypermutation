import unittest
from context import greedypermutation
# from greedypermutation import Digraph
from ds2.graph import AdjacencySetGraph as Digraph

class TestDigraph(unittest.TestCase):
    def testinit_empty(self):
        G = Digraph()

    def testinit_no_edges(self):
        G = Digraph([1,2,3])

    def testinit(self):
        G = Digraph({1,2,3}, {(1,2),(2,3)})

    def testlen(self):
        G = Digraph({1,2,3}, {(1,2)})
        self.assertEqual(len(G), 3)
        G.addvertex(3)
        self.assertEqual(len(G), 3)
        G.addvertex(4)
        self.assertEqual(len(G), 4)
        G.addedge(2,3)
        self.assertEqual(len(G), 4)

    def testhasedge(self):
        G = Digraph([1,2,3], [[1,2], [3,1]])
        self.assertTrue(G.hasedge(1,2))
        self.assertFalse(G.hasedge(2,1))
        self.assertTrue(G.hasedge(3,1))
        self.assertFalse(G.hasedge(1,3))

    def trestaddedge_missing_vertex(self):
        G = Digraph([1,2,3], [(1,2)])
        G.addedge(1,4)
        self.assertEqual(len(G), 4)

    def testcontains(self):
        G = Digraph([1,2,3,4], [(2,4), (1,3)])
        for v in [1,2,3,4]:
            self.assertTrue(v in G)
            self.assertTrue(0 not in G)
            self.assertTrue('2' not in G)

    def testremoveedge(self):
        G = Digraph([1,2,3], [(1,2), (1,3), (2,1)])
        G.removeedge(1,2)
        self.assertTrue(G.hasedge(2,1))
        self.assertTrue(G.hasedge(1,3))
        self.assertFalse(G.hasedge(1,2))

    def testremoveedge_not_an_edge(self):
        G = Digraph([1,2,3], [(1,2), (1,3), (2,1)])
        with self.assertRaises(KeyError):
            G.removeedge(3,1)

    def testvertices(self):
        G = Digraph()
        G.addvertex('a')
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('c')
        self.assertEqual(set(G.vertices()), {'a', 'b', 'c'})

    def testedges(self):
        G = Digraph([2,4,6], [(2,4), (4,6)])
        E = set(G.edges())
        self.assertEqual(len(E), 2)
        self.assertTrue((2,6) not in E and (6,2) not in E)
        G.addedge(2,6)
        E = set(G.edges())
        self.assertEqual(len(E), 3)
        self.assertTrue((2,4) in E)

if __name__ == '__main__':
    unittest.main()
