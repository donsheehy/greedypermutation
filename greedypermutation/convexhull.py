def convexhull(P):
  """ Returns the convex hull of P as a list of points

  The first point is repeated as the last point.
  This makes it easier to draw.
  """
  P = list(P)
  return lowerhull(P)[:-1] + upperhull(P)

def ccw(a,b,c):
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x) > 0

def lowerhull(P):
  P.sort(key = lambda p: (p.x, p.y))
  return grahamscan(P)

def upperhull(P):
  P.sort(key = lambda p: (-p.x, -p.y))
  return grahamscan(P)

def grahamscan(P):
  stack = []
  for p in P:
    while len(stack) >= 2 and not ccw(stack[-2], stack[-1], p):
      stack.pop()
    stack.append(p)
  return stack