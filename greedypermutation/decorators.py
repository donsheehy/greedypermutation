def greedytree_class(cls):
  def buildtree(M, seed=None, nbrconstant=1, moveconstant=1, name=None):
    BallTree = Ball(M)
    gp = greedy(M)
    class Inner(cls):
      root = greedy_tree(M, seed=seed, nbrconstant=nbrconstant, moveconstant=moveconstant)
    if name is None:
      name = cls.__name__ + '_' + M.__class__.__name__
      Inner.__name__ = Inner.__qualname__ = name
    return Inner
  return buildtree
