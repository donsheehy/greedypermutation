class Digraph:
    def __init__(self, V = (), E = ()):
        self._nbrs = {}
        for v in V:
            self.addvertex(v)
        for (u,v) in E:
            self.addedge(u,v)

    def addvertex(self, v):
        self._nbrs.setdefault(v, set())

    def addedge(self, u, v):
        self._nbrs[u].add(v)

    def vertices(self):
        return iter(self._nbrs)

    def edges(self):
        for u, nbrhood in self._nbrs.items():
            for v in nbrhood:
                yield (u,v)

    def nbrs(self, v):
        return self._nbrs[v]

    def __contains__(self, v):
        return v in self._nbrs

    def hasedge(self, u, v):
        return v in self._nbrs[u]

    def __len__(self):
        return len(self._nbrs)
