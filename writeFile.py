import networkx as nx

def writeF(G,t):

    #s = '0 7200 \n'
    s = ''
    N = G.nodes()
    N = sorted(N,reverse = False)


    for u in N:

        l = []

        if nx.is_directed(G):
            l.extend(G.predecessors(u))
            l.extend(G.successors(u))
        else:
            l.extend(G.neighbors(u))

        l = sorted(l, reverse = False)

        s = s + str(t * 600) + ' ' + str(u) + ' '

        for v in l:
            s = s + str(v) + ' '

        s = s + '\n'

    return s

def writeC(C,t):

    s = ''

    for j in range(len(C)):
        s = s + str(t * 600) + ' ' + str(j) + ' ' + str(C[j][0]) + ' ' + str(C[j][1]) + '\n'

    return s
