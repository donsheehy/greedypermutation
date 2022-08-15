from balltree import Ball

class GenericBallTree(Ball):
    def generic_search(self, candidate, viable, update):
        H = self.heap()
        for ball in H:
            candidate = update(candidate, ball)
            if not ball.isleaf():
                if viable(ball.left):
                    H.insert(ball.left)
                if viable(ball.right):
                    H.insert(ball.right)
        return candidate

    def nn(self, query):
        def update(candidate, ball):
            if ball.dist(query) < candidate.dist(query):
                return ball.center
            else:
                return candidate

        def viable(candidate, ball):
            return ball.intersects(query, candidate.dist(query))

        return self.generic_search(self.center, viable, update)

    def range_search(self, query, radius):
        def update(candidate, ball):
            if ball.isleaf():
                candidate.append(ball.center)
            return candidate

        def viable(candidate, ball):
            return ball.intersects(query, radius)

        return self.generic_search([], viable, update)

    def farthest_point(self, query):
        def update(candidate, ball):
            if ball.dist(query) > candidate.dist(query):
                return ball.center
            else:
                return candidate

        def viable(candidate, ball):
            return not ball.contained_in(query, candidate.dist(query)):

        return self.generic_search(self.center, viable, update)

    def knn(self, query, k):
        N = KNNHeap(query, k)
        N.insert(self, self.dist(query) + self.radius)

        def update(candidate, ball):
            if not ball.isleaf():
                if ball in candidate:
                    candidate.refine(ball)
                else:
                    candidate.insert(ball.left)
                    candidate.insert(ball.right)
                    candidate.tighten()
            return candidate

        def viable(candidate, ball):
            return ball.intersects(query, candidate.radius)

        for ball in self.generic_search(N, viable, update):
            if viable(N, ball):
                yield ball.center
