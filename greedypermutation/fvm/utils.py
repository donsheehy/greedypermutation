from collections import namedtuple

TreeParameters = namedtuple(
    "TreeParameters", ["move_const", "nbr_const", "tidy_const", "bucket_size"]
)

TreeParameters.__doc__ = """
The parameters for a greedy tree constructed using the Finite Voronoi Method.

move_const:     represents the lazy move parameter in the paper
nbr_const:      represents the cell approximation parameter
tidy_const:     represents the cell tidying parameter
bucket_size:    represents the parameter for a bucket queue
"""