Cluster Graph
=============

The **Cluster Graph** is a data structure that maintains a neighborhood graph on a collection of clusters and edges between them.
Each vertex is associated with a cluster of points centered at a single point.
Each cluster has a *cluster radius* equal to the largest distance from the center to a point in the cluster.

The cluster graph provides for two needs that arise when adding a new point to a greedy permutation (i.e. a new vertex in the cluster graph).
First, it limits which vertices might be considered to move into the new cluster.
Only the vertices in a neighboring cluster will be checked.
Second, it helps us quickly find the neighbors of the new cluster.
These needs translate into the following two conditions.

1. There is an edge from Cluster A to Cluster B if a point in B could be moved to the cluster of a point in A or vice versa.

2. If we add a point in A as the center of a new cluster.  Its neighbors will be a subset of the neighbors of neighbors of A.

These two conditions respectively suffice to guarantee that when a new cluster is created, we can find the points in the cluster and the neighbors.
In practice, we may keep more neighbors, relying on distances to prune away edges that cannot indicate true neighbors according to the conditions above.
Specifically, we keep edges :math:`A\to B` if the distance from :math:`A` to :math:`B` is at most the radius of :math:`A` plus the radius of :math:`b` plus the maximum of the two radii.
It's not hard to check that if this condition does not hold, then, :math:`A` and :math:`B` cannot be neighbors.

Clusters
--------

The interface to a `Cluster` is as follows.

.. autoclass:: greedypermutation.Cluster
  :members:

There are three public attributes:

- `points` an iterable collection of points.
- `center` the center point.
- `radius` the max distance between the center and a point in the cluster.

The ClusterGraph
----------------

A `ClusterGraph` is a `Graph`.

.. autoclass:: greedypermutation.ClusterGraph
  :members:
