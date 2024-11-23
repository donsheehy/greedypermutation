import logging
from greedypermutation.fvm.fvm import clarkson_fvm
from greedypermutation.fvm.ball import Ball
from greedypermutation.fvm.utils import TreeParameters
from greedypermutation.balltree import greedy_tree
from metricspaces import MetricSpace
from multiprocess import Process, Pipe
from math import sqrt

# from metricspaces import MetricSpace


def merge(tree_a, tree_b, params=TreeParameters(1,1,1,1), space=None):
    return clarkson_fvm([tree_a, tree_b], params, space)


def build_tree(P, params=TreeParameters(1,1,1,1), space=None):
    if space is None:
        space = P
    n = len(P)
    if n > 1:
        tree_1 = build_tree(P[: n // 2], params, space)
        tree_2 = build_tree(P[n // 2 :], params, space)
        # logging.debug(
        #     f"Merging greedy trees rooted at {tree_1.center} and {tree_2.center}."
        # )
        return merge(tree_1, tree_2, params)
    else:
        return Ball(space)(P[0])


def build_parallel(P, params=TreeParameters(1,1,1,1)):
    limit = max(100, sqrt(len(P)))
    space = MetricSpace([P[0]])
    return _build_parallel(P, params, limit, space)


def _build_process(
    P, params=TreeParameters(1,1,1,1), par_writer=None, limit=10, space=None
):
    out = _build_parallel(P, params, limit, space)
    par_writer.send(out)
    par_writer.close()


def _build_parallel(P, params=TreeParameters(1,1,1,1), limit=10, space=None):
    n = len(P)
    if n > limit:
        reader, writer = Pipe()
        proc = Process(
            target=_build_process,
            args=(P[: n // 2], params, writer, limit, space),
        )
        proc.start()
        tree_1 = _build_parallel(
            P[n // 2 :], params, limit, space
        )
        tree_2 = reader.recv()
        proc.join()
        reader.close()
        proc.close()
        out = merge(tree_1, tree_2, params, space)
    else:
        out = build_tree(P, params, space)
        # out = greedy_tree(P, None, nbr_const, move_const)
    return out
