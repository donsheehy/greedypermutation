from greedypermutation.fvm.fvm import clarkson_fvm
from greedypermutation.fvm.ball import Ball
# from metricspaces import MetricSpace

def merge(tree_a, tree_b, move_const=1, nbr_const=1, tidy_const=1, bucket_size=1):
    return clarkson_fvm(
        [tree_a, tree_b], move_const, nbr_const, tidy_const, bucket_size
    )

def build_tree(P, alpha, beta, delta):
    n = len(P)
    if n > 1:
        tree_1 = build_tree(P[:n//2], alpha, beta, delta)
        tree_2 = build_tree(P[n//2:], alpha, beta, delta)
        return merge(tree_1, tree_2, alpha, beta, delta, delta)
    else:
        return Ball(P)(P[0])