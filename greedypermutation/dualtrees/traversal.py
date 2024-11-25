class DualTreeSearch:
    def __init__(self, G, H):
        self.G = G
        self.H = H

    def init(self, ball):
        pass

    def update(self, node, ball):
        pass

    def cleanup(self, node):
        pass

    def __call__(self):
        for ball in self.H:
            if ball.isleaf():
                break
            self.iteration(ball)

        for a in self.G.A:
            self.cleanup(a)

    def __iter__(self):
        yield
        for ball in self.H:
            if ball.isleaf():
                break
            self.iteration(ball)
            yield

        for a in self.G.A:
            self.cleanup(a)

        yield

    def iteration(self, ball):
        left, right = ball.left, ball.right

        if ball in self.G.A:
            self.init(ball)
            self.G.add_vertices([left, right], self.G.A)
            for b in self.G.A.pop(ball):
                self.G.B[b].remove(ball)
                self.G.add_edges([(left, b), (right, b)])
            affected = {left, right}
        else:
            nbrhood = self.G.B.pop(ball)
            self.G.add_vertices([left, right], self.G.B)
            for a in nbrhood:
                self.G.A[a].remove(ball)
                self.G.add_edges([(a, left), (a, right)])
            affected = {a for a in nbrhood}

        for a in affected:
            self.update(a, ball)

        self.H.insert(left)
        self.H.insert(right)