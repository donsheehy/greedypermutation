File Formats
============

The general assumption is that data is given in files with one point per line.
The `Point` class is expected to parse the string representation of the point into a `Point` object.
The point is read up to the first semicolon.
Other data attached to a point should be included after the semicolon.
The most common form of data needed will be the index of the near predecessor.
For many applications of greedy permutations, a nearby point that came earlier in the ordering is useful.

For Euclidean points, the coordinates are separated by white space.
Here is an example for a 3D point set.

::

  2 2 0
  60 2 3
  100    12 1.9

If the point set were augmented with some predecessor pairings, we would have the following.

::

  2 2 0 ;0
  60 2 3  ; 0
  100    12 1.9 ; 1
