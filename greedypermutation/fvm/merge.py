import logging
from greedypermutation.fvm.fvm import clarkson_fvm
from greedypermutation.fvm.ball import Ball

# from metricspaces import MetricSpace


def merge(tree_a, tree_b, move_const=1, nbr_const=1, tidy_const=1, bucket_size=1):
    return clarkson_fvm(
        [tree_a, tree_b], move_const, nbr_const, tidy_const, bucket_size
    )


def build_tree(P, move_const=1, nbr_const=1, tidy_const=1, bucket_size=1):
    n = len(P)
    if n > 1:
        tree_1 = build_tree(P[: n // 2], move_const, nbr_const, tidy_const, bucket_size)
        tree_2 = build_tree(P[n // 2 :], move_const, nbr_const, tidy_const, bucket_size)
        logging.debug(
            f"Merging greedy trees rooted at {tree_1.center} and {tree_2.center}."
        )
        return merge(tree_1, tree_2, move_const, nbr_const, tidy_const, bucket_size)
    else:
        return Ball(P)(P[0])
