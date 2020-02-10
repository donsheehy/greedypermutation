from .graph import Graph

class WeightedGraph(Graph):
    def addedge(self, u, v, wt = 1):
        self._nbrs[u][v] = wt
        self._nbrs[v][u] = wt

    def addvertex(self, v):
        self._nbrs.setdefault(v, {})

    def wt(self, u, v):
        return self._nbrs[u][v]

    def dijkstra(self, v):
        tree = {}
        D = {v: 0}
        tovisit = PriorityQueue()
        tovisit.insert((None,v), 0)
        while tovisit:
            a,b = tovisit.removemin()
            if b not in tree:
                tree[b] = a
                if a is not None:
                    D[b] = D[a] + self.wt(a,b)
                for n in self.nbrs(b):
                    tovisit.add((b,n), D[b] + self.wt(b,n))
        return tree, D
