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

The interface to a Cluster is as follows.

- `__init__(self, center)` Create a new cluster with the given center.
- `addpoint(self, p)` Add the point p to the cluster.
- `updateradius(self)` Set the radius to be the distance to the farthest point from the center to a point in the cluster.
- `dist(self, other)` Return the distance between the centers of `self` and `other`.  Note, this allows `Cluster` to be treated like a point.
- `rebalance(self, other)` Move points from the cluster `other` to the cluster `self` if they are closer to the `self` center.
- `pop(self)` Return and remove the farthest point from the center.  Returns `None` if there there are no points other than the center.
- `__len__(self)` Return the total number of points in the cluster, including the center.

There are three public attributes:

- `points` a set of points.
- `center` the center point.
- `radius` the max distance between the center and a point in the cluster.

The ClusterGraph
----------------

A `ClusterGraph` is a `Graph`.
It supports the following methods.

- `__init__(self, points)` It starts with an iterable of points.  The first point will be the center of the default cluster and all other points will be placed inside.
- `addcluster(self, center)` Add a new cluster with the given center.  Update the clusters (by distance) and the edges of the graph.
- `addnextgreedypoint` - Find the next point in the greedy permutation and add a new cluster centered there. *Maybe this belongs in `clarkson.py`.*
- `closenbrs(self, u)` Iterates over the neighbors of `u` that are close enough to be real neighbors.  Any extra edges are removed.
