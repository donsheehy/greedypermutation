from .metricspace import MetricSpace
from .point import Point
from .clustergraph import Cluster, ClusterGraph

def greedy(M, seed = None):
    raise NotImplementedError

def greedytree(X):
    """ Return a greedy tree of points in # XXX:
    """
    G = ClusterGraph(X)

# def addnextgreedypoint(self):
#     parent = heappop(self._inserted)
#     newcenter = cluster.pop()
#     self.addcluster(newcenter, parent)
#     heappush(self._inserted, parent)


if __name__ == '__main__':
    X = MetricSpace(Point([x]) for x in range(100))
