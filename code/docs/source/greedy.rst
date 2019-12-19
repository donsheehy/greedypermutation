Greedy Permutations
===================

Let :math:`M` be a finite metric space, i.e., a finite set of points with a metric :math:`M\times M\to R`.
Let the points of :math:`M` be ordered :math:`p_1,\ldots, p_n`.
Let :math:`P_i:= \{p_1,\ldots, p_i\}`.
This ordering is *greedy* if for all :math:`i = 2\ldots n`, we have
.. math::
  d(p_i, P_{i-1}) = \max_{q\in M} d(p_i, P_{i-1})
