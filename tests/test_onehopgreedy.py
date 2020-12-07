import pytest
from greedypermutation import Point
from greedypermutation.onehopgreedy import onehopgreedy
from metricspaces import MetricSpace

def test_points_on_a_line():
    P = [Point([i]) for i in range(100)]
    GP = list(onehopgreedy(MetricSpace(P), P[50]))
    assert(GP[0] == P[50])
    expected = [50, 16, 83]
    n = len(expected)
    assert(GP[:n] == [P[i] for i in expected])



if __name__ == '__main__':
    pytest.main()
