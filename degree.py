import matplotlib.pyplot as plt

def deg(G):

    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1


    plt.plot(X,Y)
    plt.show()

