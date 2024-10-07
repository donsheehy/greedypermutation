import logging
from greedypermutation.fvm.ball import Ball
from greedypermutation.fvm.neighborgraph import GreedyNeighborGraph
from metricspaces import MetricSpace

logging.basicConfig(level=logging.NOTSET)

# Clarkson's algorithm on greedy tree nodes.


def clarkson_fvm(
    inp_trees: list[Ball],
    move_const: float = 1.0,
    nbr_const: float = 1.0,
    tidy_const: float = 1.0,
    bucket_size: float = 1.0,
    e: float = 0.0,
) -> Ball:
    nbr_graph = GreedyNeighborGraph(
        inp_trees, nbr_const, move_const, tidy_const, bucket_size
    )
    leaf = {}
    out_tree = None
    for p, pred in _sites(inp_trees, nbr_graph):
        logging.info(
            f"Next point is {(p.x, p.y)} with predecessor {None if pred is None else (pred.x, pred.y)}."
        )
        if pred is None:
            BallTree = Ball(MetricSpace([p]))
            out_tree = BallTree(p)
            leaf[p] = out_tree
        else:
            left_leaf, right_leaf = BallTree(pred), BallTree(p)
            leaf[pred].left, leaf[pred].right = left_leaf, right_leaf
            leaf[pred], leaf[p] = left_leaf, right_leaf
        logging.info(f"Leaves: {[str(l) for l in leaf]}")
        logging.info(out_tree)
        
    logging.info(f"Leaves: {[str(l) for l in leaf]}")
    logging.info(out_tree)
    # Compute node radii
    out_tree.update()
    return out_tree


def _sites(inp_trees, nbr_graph):
    heap = nbr_graph.heap
    root = heap.findmax()

    yield root.center, None
    logging.info("Now beginning loop.")
    for _ in range(1, sum(len(inp_tree) for inp_tree in inp_trees)):
        cell = heap.findmax()
        logging.info(f"Max cell: {cell.center}, {cell.outradius}")
        node = cell.farthest
        nbr_graph.addcell(node, cell)
        yield node.center, cell.center
