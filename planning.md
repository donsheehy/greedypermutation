# greedypermutation Planning

## Documentation

- [ ] Document the quadratic algorithm
- [ ] Include examples and figures in the docs
- [ ] Give CLI example usage

## Factor out all the metric space stuff

This is coming along.  There is still an unknown error in the CLI tests.  It must be because it calls `add` and `fromstrings` on the metric space.

## Provide a mechanism for importing metric for the CLI

## knnsample returns the tree

This should help with testing.
It should make it possible to quickly check that each point was really justified according to the greedy algorithm definition.
