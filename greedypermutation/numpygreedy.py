import numpy as np
from scipy.spatial.distance import cdist

def greedy(P):
    S = cdist(P, P, 'sqeuclidean')
    D = S[0]
    j = 0
    for _ in P:
        yield P[j]
        j = D.argmax()
        D = np.minimum(S[j], D)
