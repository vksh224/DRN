import matplotlib.pyplot as plt

def degree_dist(G,fname):

    m_id = max([G.in_degree(u) for u in G.nodes()])
    m_od = max([G.out_degree(u) for u in G.nodes()])

    od = [0 for _ in range(m_od + 1)]
    id = [0 for _ in range(m_id + 1)]

    for u in G.nodes():
        od[G.out_degree(u)]+= 1
        id[G.in_degree(u)] += 1

    plt.figure(1)
    plt.subplot(211)
    plt.plot(range(len(id)),id)

    plt.subplot(212)
    plt.plot(range(len(od)),od)

    plt.savefig(fname + '.png')


