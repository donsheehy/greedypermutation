import unittest
from greedypermutation import MetricSpace, Point

class TestMetricSpace(unittest.TestCase):
    def testinitmetricspace(self):
        P = [Point([a]) for a in [3,7,9,2,1]]
        M = MetricSpace(P)

if __name__ == '__main__':
    unittest.main()
