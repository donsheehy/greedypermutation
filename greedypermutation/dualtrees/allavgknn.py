from collections import defaultdict
from greedypermutation.dualtrees.allknn import AllKNN

class AllAvgKNN(AllKNN):
    def __init__(self, G_A, G_B, k, e=0):
        super().__init__(G_A, G_B, k, e)
        self.out = defaultdict(float)
        self.acc = defaultdict(float)
        self.num = defaultdict(int)
        self.acc[G_A] =self.num[G_A] = 0

    def init(self, ball):
        super().init(ball)
        left, right = ball.left, ball.right
        self.acc[left] = self.acc[right] = self.acc.pop(ball)
        self.num[left] = self.num[right] = self.num.pop(ball)
        
    def accumulate(self, a):
        nbrhood = {b for b in self.G.A[a]}
        for b in nbrhood:
            if self.closeby(a, b) and self.accumulable(a, b):
                self.acc[a] = (self.acc[a]*self.num[a] + (a.dist(b.center) - a.radius - b.radius)*len(b))/(self.num[a] + len(b))
                self.num[a] += len(b)
                self.G.remove_edge(a, b)

    def closeby(self, a, b):
        ub = self.knn_heaps[a].radius
        farthest = self.knn_heaps[a].findmax()
        lb = ub - 2*farthest.radius
        return True if a.dist(b.center) <= lb - 2*a.radius - b.radius else False

    def accumulable(self, a, b):
        if self.e == 0:
            return True if a.radius == b.radius == 0 else False
        else:
            return True if a.dist(b.center) >= (2+self.e)/(self.e)*(a.radius + b.radius) else False

    def finish(self, a):
        nbrhood = {b for b in self.G.A[a]}
        if len(nbrhood) == 0:
            for p in a:
                self.out[p] = self.acc[a]

    def update(self, node, ball):
        self.update_candidates(node, ball)
        self.prune(node)
        self.accumulate(node)
        self.finish(node)


if __name__ == '__main__':
    from metricspaces import MetricSpace, R1
    from greedypermutation.balltree import greedy_tree

    A = list(range(2,15,3))
    B = list(range(1,20,4))
    knn = 3

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], knn)
    print([b for b in B])
    avgknn = AllAvgKNN(G_A, G_B, knn)
    output = avgknn()
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        print(f'{pt}: dist: {output[pt]}')

    A = [1,2,3,6,7,8]
    B = [1,2,3,6,7,9]
    knn = 4

    G_A = greedy_tree(MetricSpace(A, pointclass = R1))
    G_B = greedy_tree(MetricSpace(B, pointclass = R1))

    print([a for a in A], knn)
    print([b for b in B])
    avgknn = AllAvgKNN(G_A, G_B, knn)
    output = avgknn()
    for pt in output:
        # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
        # print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')
        print(f'{pt}: dist: {output[pt]}')

    print("okay!")
