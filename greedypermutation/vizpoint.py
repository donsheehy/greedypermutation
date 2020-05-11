from ds2viz.element import Circle

class VizPoint(Circle):
    def __init__(self, x, y, radius = 1):
        super().__init__(radius)
        self.x, self.y = x, y
        self.align('center', (x,y))

    def __iter__(self):
        yield self.x
        yield self.y

    def dist(self, other):
        return sum((a-b) ** 2 for a,b in zip(self, other)) ** (0.5)

    def __eq__(self, other):
        return list(self) == list(other)

    def __hash__(self):
        return hash((self.x, self.y))
