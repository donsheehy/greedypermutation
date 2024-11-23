import logging
from metricspaces import MetricSpace
from greedypermutation.fvm.ball import Ball
from greedypermutation.fvm.utils import TreeParameters
from greedypermutation.fvm.neighborgraph import GreedyNeighborGraph

# Clarkson's algorithm on greedy tree nodes.
def clarkson_fvm(
    inp_trees: list[Ball],
    params: TreeParameters = TreeParameters(1,1,1,1),
    space: MetricSpace = None
) -> Ball:
    move_const, nbr_const, tidy_const, bucket_size = params
    if space is None:
        space = MetricSpace(inp_trees[0].center)
    nbr_graph = GreedyNeighborGraph(inp_trees, params, space)
    leaf = {}
    out_tree = None
    for p, pred in _sites(inp_trees, nbr_graph):
        if pred is None:
            BallTree = Ball(space)
            BallTree.scale = move_const / (tidy_const * bucket_size)
            BallTree.gp = nbr_const * tidy_const * bucket_size
            out_tree = BallTree(p)
            leaf[p] = out_tree
        else:
            node = leaf[pred]
            left, right = BallTree(pred), BallTree(p)
            node.left, node.right = left, right
            leaf[pred], leaf[p] = left, right

    out_tree.count()
    # Compute node radii
    if out_tree.scale > 1:
        # logging.debug("Computing approximate radii")
        out_tree.approx_radii()
    else:
        # logging.debug("Computing exact radii")
        out_tree.exact_radii()
    return out_tree


def _sites(inp_trees, nbr_graph):
    heap = nbr_graph.heap
    root = heap.findmax()

    yield root.center, None
    for _ in range(1, sum(len(inp_tree) for inp_tree in inp_trees)):
        cell = heap.findmax()
        logging.debug(f"Max cell: {cell.center} with outradius {cell.outradius}")
        newcenter = cell.farthest.center
        nbr_graph.addcell(newcenter, cell)
        yield newcenter, cell.center
