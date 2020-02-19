from .digraph import Digraph

class Graph(Digraph):
    def addedge(self, u, v):
        Digraph.addedge(self, u, v)
        Digraph.addedge(self, v, u)

    def removeedge(self, u, v):
        Digraph.removeedge(self, u, v)
        Digraph.removeedge(self, v, u)

    def edges(self):
        for u, nbrhood in self._nbrs.items():
            for v in nbrhood:
                if u < v:
                    yield (u,v)

    def removeedge(self, u, v):
        """ Remove the edge (u,v).
        This will raise a KeyError if the edge (u,v) is not already in the graph.
        """
        self._nbrs[u].remove(v)
        if u is not v:
            self._nbrs[v].remove(u)
