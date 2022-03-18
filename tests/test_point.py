import unittest
from greedypermutation import Point

class TestPoint(unittest.TestCase):
    def test_init_2D_points(self):
        # Just checking that init doesn't crash
        Point([0,0])
        Point([-1,2])
        Point([-1.1, 2.99])

    def testlen(self):
        P = [Point([1]), Point([1,2]), Point([1,2,3])]
        self.assertEqual(len(P[0]), 1)
        self.assertEqual(len(P[1]), 2)
        self.assertEqual(len(P[2]), 3)

    def test_init_with_other_iterables(self):
        p = Point(range(100))
        self.assertEqual(len(p), 100)

    def test_dist_1D(self):
        P = [Point([i]) for i in range(10)]
        self.assertEqual(P[1].dist(P[5]), 4)
        self.assertEqual(P[5].dist(P[1]), 4)
        self.assertEqual(P[0].dist(P[9]), 9)
        self.assertEqual(P[1].dist(P[1]), 0)
        self.assertEqual(P[6].dist(P[8]), 2)

    def test_dist_2D(self):
        a = Point([1,3])
        b = Point([13,8])
        self.assertEqual(a.dist(b), 13)

    def test_dist_with_different_dimensions(self):
        """If two points are in different dimensions, the higher dimensional
        point should be projected to the lower dimensional space.
        """
        p, q = Point([3,4]), Point([0])
        self.assertEqual(p.dist(q), 3)
        r = Point([0,0,100])
        self.assertEqual(p.dist(r), 5)

    def test_eq(self):
        a = Point([3,4])
        b = Point([3.0, 4.0])
        self.assertTrue(a == b)

    def test_hash(self):
        a = Point([30000000000,4])
        b = Point([30000000000.0, 4.0])
        self.assertEqual(hash(a), hash(b))

    def test_fromstring(self):
        p = Point.fromstring("  4  2.01 999")
        self.assertEqual(len(p), 3)
        a = Point.fromstring(' 3  4  12')
        self.assertEqual(len(a), 3)
        b = Point([0,0,0])
        self.assertEqual(a.dist(b), 13)

    def test_iter(self):
        p = Point(3* i for i in range(4))
        for i, c in enumerate(p):
            self.assertEqual(c, 3 * i)

if __name__ == '__main__':
    unittest.main()
