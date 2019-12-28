import unittest
from context import greedypermutation
from greedypermutation import Graph

class TestGraph(unittest.TestCase):
    def testinit_empty(self):
        G = Graph()

    def testinit_no_edges(self):
        G = Graph([1,2,3])

    def testinit(self):
        G = Graph({1,2,3}, {(1,2),(2,3)})

    def testlen(self):
        G = Graph({1,2,3}, {(1,2)})
        self.assertEqual(len(G), 3)
        G.addvertex(3)
        self.assertEqual(len(G), 3)
        G.addvertex(4)
        self.assertEqual(len(G), 4)
        G.addedge(2,3)
        self.assertEqual(len(G), 4)

    def testcontains(self):
        G = Graph([1,2,3,4], [(2,4), (1,3)])
        for v in [1,2,3,4]:
            self.assertTrue(v in G)
        self.assertTrue(0 not in G)
        self.assertTrue('2' not in G)

    def testhasedge(self):
        G = Graph([1,2,3], [[1,2]])
        self.assertTrue(G.hasedge(1,2))
        self.assertTrue(G.hasedge(2,1))
        self.assertFalse(G.hasedge(1,3))

    def trestaddedge_missing_vertex(self):
        G = Graph([1,2,3], [(1,2)])
        G.addedge(1,4)
        self.assertEqual(len(G), 4)

    def testvertices(self):
        G = Graph()
        G.addvertex('a')
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('c')
        self.assertEqual(set(G.vertices()), {'a', 'b', 'c'})

    def testedges(self):
        G = Graph([2,4,6], [(2,4), (4,6)])
        E = set(G.edges())
        self.assertEqual(len(E), 2)
        self.assertTrue({2,6} not in E and {6,2} not in E)
        G.addedge(2,6)
        E = set(G.edges())
        self.assertEqual(len(E), 3)
        self.assertTrue({2,4} in E)

if __name__ == '__main__':
    unittest.main()
