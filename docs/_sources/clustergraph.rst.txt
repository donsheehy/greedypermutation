Cluster Graph
=============

The **Cluster Graph** is a data structure that maintains a neighborhood graph on a collection of clusters.
Each vertex is associated with a cluster of points centered at a single point.
Each cluster has a *cluster radius* equal to the largest distance from the center to a point in the cluster.
The graph itself also has a *graph radius* that determines its edges.
The graph radius is always at least as large as the largest cluster radius.
Two clusters are neighbors in the cluster graph if the distance between their centers is less than three times the graph radius.

The cluster graph provides for two needs that arise when adding a new point to a greedy permutation (i.e. a new vertex in the cluster graph).
First, it limits which vertices might be considered to move into the new cluster.
Only the vertices in a neighboring cluster will be checked.
Second, it helps us quickly find the neighbors of the new cluster.
These needs translate into the following two conditions.

Clusters A and B are neighbors if a point in A could be moved to the cluster of a point in B (or vice versa).

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
