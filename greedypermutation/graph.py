from .digraph import Digraph

class Graph(Digraph):
    def addedge(self, u, v):
        Digraph.addedge(self, u, v)
        Digraph.addedge(self, v, u)

    def removeedge(self, u, v):
        Digraph.removeedge(self, u, v)
        Digraph.removeedge(self, v, u)
