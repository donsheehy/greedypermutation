from random import randrange, seed
from greedypermutation.dualtrees.allrange import AllRange
from greedypermutation.dualtrees.allknn import AllKNN
from ds2viz.geometry import VizPoint as Point
from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt

fn_set = {AllRange, AllKNN}


def compute_degrees(A, B, G_A, G_B, fn, **kwargs):
    if fn not in fn_set:
        print("Invalid search function")
        return

    def append_degrees(degrees, points, vertices):
        centers = {p.center: p for p in vertices}
        for p in points:
            degrees[p].append(0 if p not in centers else len(vertices[centers[p]]))

    def to_nparray(degrees):
        return np.array([np.array(degrees[point]) for point in degrees])

    degree_a = defaultdict(list)
    degree_b = defaultdict(list)

    search = fn(G_A, G_B, **kwargs)
    for output in search:
        G = output[0]
        append_degrees(degree_a, A, G.A)
        append_degrees(degree_b, B, G.B)

    return to_nparray(degree_a), to_nparray(degree_b)


def max_degree(degrees):
    iterwise = np.array([np.max(col) for col in degrees.T])
    pointwise = np.array([np.max(row) for row in degrees])
    return iterwise, pointwise


def avg_degree(degrees):
    inserted = set()
    iterwise = []
    for col in degrees.T:
        active = []
        for i, x in enumerate(col):
            if x != 0 or i in inserted:
                inserted.add(i)
                active.append(x)
        iterwise.append(sum(active) / len(active) if len(active) > 0 else 0)

    iterwise = np.array(iterwise)
    # iterwise = np.array([np.avg(np.trim_zeros(col, 'fb') for col in degrees.T)])
    pointwise = np.array(
        [
            0 if len(np.trim_zeros(row, "f")) == 0 else np.mean(np.trim_zeros(row, "f"))
            for row in degrees
        ]
    )
    return iterwise, pointwise


def analyze(A, B, G_A, G_B, fn, **kwargs):
    # n_a = len(A)
    # n_b = len(B)

    deg_a, deg_b = compute_degrees(A, B, G_A, G_B, fn, **kwargs)

    max_a_iter, max_a_point = max_degree(deg_a)
    max_b_iter, max_b_point = max_degree(deg_b)

    avg_a_iter, avg_a_point = avg_degree(deg_a)
    avg_b_iter, avg_b_point = avg_degree(deg_b)

    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(max_a_iter, color="red", label="max_a")
    ax.plot(max_b_iter, color="blue", label="max_b")
    ax.plot(avg_a_iter, color="red", linestyle="dashed", label="avg_a")
    ax.plot(avg_b_iter, color="blue", linestyle="dashed", label="avg_b")
    ax.legend()
    ax.set_title("Degrees per iteration")

    ax = fig.add_subplot(2, 2, 3)
    # ax.scatter(range(n_a), max_a_point, color='red', label='max_a')
    # ax.scatter(range(n_a), avg_a_point, color='red', facecolors='none', label='avg_a')
    ax.plot(max_a_point, color="red", label="max_a")
    ax.plot(avg_a_point, color="red", linestyle="dashed", label="avg_a")
    ax.legend()
    ax.set_title("Degrees per point in A")

    ax = fig.add_subplot(2, 2, 4)
    # ax.scatter(range(n_b), max_b_point, color='blue', label='max_b')
    # ax.scatter(range(n_b), avg_b_point, color='blue', facecolors='none', label='avg_b')
    ax.plot(max_b_point, color="blue", label="max_b")
    ax.plot(avg_b_point, color="blue", linestyle="dashed", label="avg_b")
    ax.legend()
    ax.set_title("Degrees per point in B")

    plt.show(block=True)


if __name__ == "__main__":
    from metricspaces import MetricSpace
    from greedypermutation.balltree import greedy_tree

    W = 5000
    H = 3000

    N_A = 100
    N_B = 100
    R = 300
    K = 4
    STOP = 50

    seed(10)

    def randompoint(xx, yy):
        return Point(randrange(*xx), randrange(*yy))

    A = {randompoint((50, W - 50), (50, H - 50)) for i in range(N_A)}
    B = {randompoint((50, W - 50), (50, H - 50)) for i in range(N_B)}
    G_A = greedy_tree(MetricSpace(A))
    G_B = greedy_tree(MetricSpace(B))

    # analyze(A, B, G_A, G_B, AllRange, r=R)
    analyze(A, B, G_A, G_B, AllKNN, k=K)
    # deg_a, deg_b, output = compute_degrees(A, B, G_A, G_B, all_knn_analyze, k=5, epsilon=0)

    # print(deg_a)
    # print(deg_b)
    # for pt in output:
    #     print(f'{pt}: dist: {output[pt][0]}, nbr: {output[pt][1]}')
    # print(f'{pt}: {[(a.center, a.radius, len(a)) for a in output[pt]]}')
