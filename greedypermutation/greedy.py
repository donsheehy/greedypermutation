from metricspace import MetricSpace
from point import Point
from sys import stdin

M = MetricSpace()
M.fromstrings(stdin, Point.fromstring)
for p, i in M.greedytree():
    print(str(p), ';', i)
