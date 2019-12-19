Greedy Permutations
===================

Let :math:`M` be a finite metric space, i.e., a finite set of points with a metric :math:`M\times M\to R`.
Let the points of :math:`M` be ordered :math:`p_1,\ldots, p_n`.
Let :math:`P_i:= \{p_1,\ldots, p_i\}`.
This ordering is *greedy* if for all :math:`i = 2\ldots n`, we have

.. math::
  d(p_i, P_{i-1}) = \max_{q\in M} d(p_i, P_{i-1}).

The greedy permutation is not unique.
Given any choice of the first point, it is always possible to complete the ordering to be greedy.
It also implies an algorithm.
At step :math:`i`, set :math:`p_i` to be the farthest point to :math:`P_{i-1}` among all the remaining points.
This is not very efficient.
It would take :math:`(n-i+1)(i-1)` distance computations to determine the :math:`i`th point.
