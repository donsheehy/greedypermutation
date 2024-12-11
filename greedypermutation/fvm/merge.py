from greedypermutation.fvm.fvmgreedy import fvm_greedy
from greedypermutation.fvm.simpleball import SimpleBall
from greedypermutation.fvm.utils import TreeParameters
from metricspaces import MetricSpace
from multiprocess import Process, Pipe
from math import sqrt


def merge(tree_a, tree_b, params=TreeParameters(1, 1, 1, 1), space=None):
    """
    Merges two greedy trees into a single tree.
    """
    return fvm_greedy([tree_a, tree_b], params, space)


def build_tree(P, params=TreeParameters(1, 1, 1, 1), space=None):
    """
    An implementation of the sequential recursive algorithm to build a greedy tree on a finite metric space `P`.
    The parameters are move_const, nbr_const, tidy_const, and, bucket_size.
    All of these default to one.
    The move_constant represents the lazy move parameter in the paper.
    Similarly, the nbr_constant represents the cell approximation parameter.
    The tidy_constant represents the cell tidying parameter.
    The bucket_size represents the parameter for a bucket queue.
    """
    if space is None:
        space = MetricSpace([P[0]])
    n = len(P)
    if n > 1:
        tree_1 = build_tree(P[: n // 2], params, space)
        tree_2 = build_tree(P[n // 2 :], params, space)
        return merge(tree_1, tree_2, params)
    else:
        return SimpleBall(space)(P[0])


def build_parallel(P, params=TreeParameters(1, 1, 1, 1)):
    """
    An implementation of the parallel algorithm to build a greedy tree on a finite metric space `P`.
    The parameters are the same as those for `build_tree`.
    """
    limit = max(100, sqrt(len(P)))
    space = MetricSpace([P[0]])
    return _build_parallel(P, params, limit, space)


def _build_process(
    P, params=TreeParameters(1, 1, 1, 1), par_writer=None, limit=10, space=None
):
    out = _build_parallel(P, params, limit, space)
    par_writer.send(out)
    par_writer.close()


def _build_parallel(P, params=TreeParameters(1, 1, 1, 1), limit=10, space=None):
    n = len(P)
    if n > limit:
        reader, writer = Pipe()
        proc = Process(
            target=_build_process,
            args=(P[: n // 2], params, writer, limit, space),
        )
        proc.start()
        tree_1 = _build_parallel(P[n // 2 :], params, limit, space)
        tree_2 = reader.recv()
        proc.join()
        reader.close()
        proc.close()
        out = merge(tree_1, tree_2, params, space)
    else:
        out = build_tree(P, params, space)
    return out
