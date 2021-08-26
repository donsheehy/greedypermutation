Clarkson's Algorithm
====================

The basic algorithm for computing a greedy permutation is to insert the points one at a time, keeping track of the reverse nearest neighbors of each point.
Adding a new point takes linear time and then updating the reverse nearest neighbors takes linear time.
Thus, the entire construction takes quadratic time.
There is a clear opportunity for improvement in this algorithm; adding a new point requires checking points that are far away to see if their nearest neighbor has changed.
If the new point is far away, we'd like to skip this check.

The following approach attributed to Clarkson reduces these checks (See :cite:`clarkson97nearest`, :cite:`clarkson99nearest`,  :cite:`clarkson03nearest`).
The variation we present resembles more closely the presentation in Har-Peled and Mendel :cite:`har-peled06fast`.
It is incremental.
After :math:`i` points are added, the *current radius* is the distance from the last point added to its nearest predecessor.
The main idea is to maintain a graph whose vertex set is the current set of inserted points.
Each defines a cell.
Two vertices are neighbors in this graph if their distance is less than three times the current radius.
After each insertion, the only points that move (i.e., have new nearest neighbors) are those that are in cells adjacent to the cell of the new point.
This eliminates many checks.
Moreover, the neighbors of the new cell are also found among the neighbors of the cell of the new point.
The implementation of this algorithm uses the `NeighborGraph` data structure.



.. bibliography:: references.bib
