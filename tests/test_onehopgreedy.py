import pytest
from greedypermutation import (Point,
                               MetricSpace,
                               )
from greedypermutation.onehopgreedy import onehopgreedy

def test_points_on_a_line():
    P = [Point([i]) for i in range(100)]
    GP = list(onehopgreedy(MetricSpace(P), P[50]))
    # assert(GP[0] == P[0])
    # assert(GP[1] == P[50])
    expected = [0, 50, 75, 13, 88, 40, 20, 57, 94]
    expected = [50, 24, 75, 11, 88]
    n = len(expected)
    assert(GP[:n] == [P[i] for i in expected])



if __name__ == '__main__':
    pytest.main()
