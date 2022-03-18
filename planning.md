# greedypermutation Planning

## The `point` class should instead use the one in MetricSpaces

This would also allow us to use other Lp distances.

## Documentation

- [ ] Document the quadratic algorithm
- [ ] Include examples and figures in the docs
- [ ] Give CLI example usage

## Something looks funny in the weights update

I think the weight update should be in a separate loop or it should simply add the weight of each child as it goes.

## Factor out all the metric space stuff

This is coming along.  There is still an unknown error in the CLI tests.  It must be because it calls `add` and `fromstrings` on the metric space.

## Provide a mechanism for importing metric for the CLI

## knnsample returns the tree

This should help with testing.
It should make it possible to quickly check that each point was really justified according to the greedy algorithm definition.
