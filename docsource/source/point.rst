A Generic Point
===============

We want a very generic point class that will provide everything needed to be used as part of a metric space.
It must implement the following methods:

- `dist(self, other)` This is distance function, i.e. the metric.
- `fromstring` We will use this to parse data files from the command line.
- `__eq__` We need to know if two points are the same point.
- `__hash__` We will often want to store sets of points and thus Points must be hashable.
- `__str__` It is often useful to print the points.

These will be our basic requirements for a `Point` class.
If you want to define your own metric to use with this package, it need only implement these methods in order to work.
