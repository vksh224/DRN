import networkx as nx

def tiers(G,N,t1,t2,t3):

    if t1 == [] or t2 == [] or t3 == []:
        if N == None:
            N = G.nodes()

        for u in N:

            if G.out_degree(u) == 0:
                t1.append(u)

            elif G.out_degree(u) > 0 and G.in_degree(u) > 0:
                t2.append(u)

            else:
                t3.append(u)

        return t1,t2,t3

    t1_M = [each for each in N if each in t1]
    t2_M = [each for each in N if each in t2]
    t3_M = [each for each in N if each in t3]

    return t1_M,t2_M,t3_M

def find_tier_degree(curr_node,t,G):

    listnodes = []

    for u in t:
        if G.has_edge(curr_node,u) or G.has_edge(u,curr_node):
            listnodes.append(u)

    return listnodes


