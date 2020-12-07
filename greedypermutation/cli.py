import click
import os
from greedypermutation import Point
from metricspaces import MetricSpace

@click.command()
@click.argument('pointsfile', type = click.File('r'))
# @click.option('--outfile', type = click.Path(allow_dash = True),
@click.option('--outfile', type = click.File('w'),
                default = '-',
                help = "Where to store the output.")
@click.option('--algorithm',
                type=click.Choice(['clarkson', 'quadratic'], case_sensitive=False),
                default = 'clarkson',
                help='Which algorithm to use: `quadratic` or `clarkson`.')
@click.option('--tree/--notree', default = True,
                help='Include the entire tree in the output or not.')
def cli(pointsfile, outfile, algorithm, tree):
    """
    Compute a greedy permutation of the points in the `pointsfile`.

    The output will be saved to the file specified by `outfile`.

    By default it will run the Clarkson algorithm.
    If `--algorithm quadratic` is specified, then the quadratic algorithm will
    be used.

    The `--tree` and `--notree flags determine if the tree is included in the
    output.  This is managed by appending the index of the predecessor after
    a semicolon.
    """
    M = MetricSpace()
    M.fromstrings(pointsfile.readlines(), Point.fromstring)

    if algorithm == 'quadratic':
        import greedypermutation.quadraticgreedy as algo
    else:
        import greedypermutation.clarksongreedy as algo
    if tree:
        for p, i in algo.greedy(M, tree = True):
            outfile.write(str(p) + ';' + str(i) + '\n')
    else:
        for p in algo.greedy(M):
            outfile.write(str(p) + '\n')
