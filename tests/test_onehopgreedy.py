import unittest
from greedypermutation import Point
from greedypermutation.onehopgreedy import onehopgreedy
from metricspaces import MetricSpace


class TestOneHopGreedy(unittest.TestCase):
    def test_points_on_a_line(self):
        P = [Point([i]) for i in range(100)]
        GP = list(onehopgreedy(MetricSpace(P), P[50]))
        self.assertEqual(GP[0], P[50])
        expected = [50, 16, 83]
        n = len(expected)
        self.assertEqual(GP[:n], [P[i] for i in expected])


if __name__ == '__main__':
    unittest.main()
