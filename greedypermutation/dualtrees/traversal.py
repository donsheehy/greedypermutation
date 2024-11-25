def dualtree_iteration(G, H, init, update, ball):
    left, right = ball.left, ball.right

    if ball in G.A:
        init(ball)
        G.add_vertices([left, right], G.A)
        for b in G.A.pop(ball):
            G.B[b].remove(ball)
            G.add_edges([(left, b), (right, b)])
        affected = {left, right}
    else:
        nbrhood = G.B.pop(ball)
        G.add_vertices([left, right], G.B)
        for a in nbrhood:
            G.A[a].remove(ball)
            G.add_edges([(a, left), (a, right)])
        affected = {a for a in nbrhood}

    for a in affected:
        update(a, ball)

    H.insert(left)
    H.insert(right)

# def dualtree_search(G, H, init, update, cleanup):
#     for ball in H:
#         if ball.isleaf():
#             break
#         left, right = ball.left, ball.right

#         if ball in G.A:
#             init(ball)
#             for b in G.A.pop(ball):
#                 G.B[b].remove(ball)
#                 G.add_edges([(left, b), (right, b)])
#             affected = {left, right}
#         else:
#             for a in G.B.pop(ball):
#                 G.A[a].remove(ball)
#                 G.add_edges([(a, left), (a, right)])
#             affected = {a for a in G.B[left]}

#         for a in affected:
#             update(a, ball)

#         H.insert(left)
#         H.insert(right)

#     for a in G.A:
#         cleanup(a)

def dualtree_search(G, H, init, update, cleanup):
    for ball in H:
        if ball.isleaf():
            break
        dualtree_iteration(G, H, init, update, ball)

    for a in G.A:
        cleanup(a)

def dualtree_analysis(G, H, init, update, cleanup):
    yield
    for ball in H:
        if ball.isleaf():
            break
        dualtree_iteration(G, H, init, update, ball)
        yield

    for a in G.A:
        cleanup(a)

    yield