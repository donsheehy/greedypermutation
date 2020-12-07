import unittest
from greedypermutation import Point, knnsample
from metricspaces import MetricSpace

class TestKNNSample(unittest.TestCase):
    def test_smallinstance(self):
        k = 11
        # S = set(range(0, 100, 4))
        S = set(range(0,100,4)) | set(range(100, 200, 10))
        P = [Point([c]) for c in S]
        M = MetricSpace(P)
        output = list(knnsample(M, k, P[0]))
        print(len(output), output)
        self.assertTrue(len(output) >= len(S) / k)


if __name__ == '__main__':
    unittest.main()
