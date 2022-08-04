import numpy as np
from scipy.spatial.distance import cdist


def greedy(P, distance='sqeuclidean'):
    S = cdist(P, P, distance)
    D = S[0]
    j = 0
    for _ in P:
        yield P[j]
        j = D.argmax()
        D = np.minimum(S[j], D)


def sample(P, delta, distance='sqeuclidean'):
    S = cdist(P, P, distance)
    D = S[0]
    j = 0
    output = []
    for _ in P:
        output.append(P[j])
        j = D.argmax()
        if D[j] < delta:
            return output
        D = np.minimum(S[j], D)
