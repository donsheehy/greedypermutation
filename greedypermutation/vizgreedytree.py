from ds2viz.element import Group, Line
from greedypermutation.maxheap import MaxHeap
from greedypermutation.vizpoint import VizPoint

class VizGreedyTree(Group):
    def __init__(self, T):
        super().__init__()
        P = set()
        for p, q in T:
            P.add(p)
            if q is not None:
                self.addelement(Line(p, q))
        for p in P:
            self.addelement(VizPoint(*p))
