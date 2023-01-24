"""
Intended usage example:
>>> g = GreedyTreeClass(X, seed=Point((1,2)), nbrconstant=2, moveconstant=2)
>>> g.refine(param)
"""

@greedytree_class
class GreedyTreeClass:
  @classmethod
  def refine(cls, param):
    pass

  @classmethod
  def merge(cls, other):
    pass

  @classmethod
  def delete(cls, point):
    pass

