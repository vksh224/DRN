import math
import networkx as nx
import numpy as np
import pickle

from operator import itemgetter


def check(u_w,u_g,mapped_wsn,mapped_grn,undirected,directed,fidelity):

    den = 0.0
    num = 0.0

    #path-per-edge
    ppe = 0.0
    den1 = 0.0
    e = []
    for i in range(len(mapped_wsn)):

        if undirected.has_edge(u_w,mapped_wsn[i]):
            den += 1.0
            # if directed.has_edge(u_g,mapped_grn[i]):
            if nx.has_path(directed, u_g, mapped_grn[i]):
                num += 1.0
                e.append((u_w,mapped_wsn[i]))
                ppe += nx.shortest_path_length(directed,source = u_g,target = mapped_grn[i])
                den1 += 1.0
            # elif directed.has_edge(mapped_grn[i], u_g):
            elif nx.has_path(directed, mapped_grn[i], u_g):
                num += 1.0
                e.append((mapped_wsn[i],u_w))
                ppe += nx.shortest_path_length(directed,source = mapped_grn[i],target = u_g)
                den1 += 1.0

    if den == 0:
        return [],0,ppe,den

    p = float(num)/float(den)

    if  p >= fidelity:
        return e,1,ppe,den1
    else:
        return [],0,ppe,den1

def embed_map(directed,undirected,r_directed,r_undirected,fidelity):

    mapped_grn = []
    mapped_wsn = []

    #print len(directed),len(directed.edges())
    #print len(undirected),len(undirected.edges())

    #1. Arrange the GRN and WSN nodes in the decreasing order of ranks

    r_directed = [each[0] for each in sorted(r_directed.items(), key=itemgetter(1),reverse = True)]
    r_undirected = [each[0] for each in sorted(r_undirected.items(), key=itemgetter(1), reverse = True)]

    #print (r_directed)
    #print (r_undirected)

    #r_directed = sorted(range(len(r_directed)), key = lambda k:r_directed[k], reverse = True)
    #r_undirected = sorted(range(len(r_undirected)), key = lambda k:r_undirected[k], reverse = True)

    iter = 0

    first = False
    for u_w in r_undirected:
        for u_g in r_directed:

            #Map the highest ranked node to the highest ranking gene s.t. former's degree is less than or equal to the latter.
            if undirected.degree(u_w) <= directed.in_degree(u_g) + directed.out_degree(u_g):
                mapped_grn.append(u_g)
                mapped_wsn.append(u_w)
                first = True

            if first:
                break
        if first:
            break

    E = []
    ppe = 0.0
    den = 0.0
    for u_w in r_undirected:
        iter += 1
        for u_g in r_directed:
            if u_w in mapped_wsn or u_g in mapped_grn:
                continue

            e,decision,ppe,den = check(u_w,u_g,mapped_wsn,mapped_grn,undirected,directed,fidelity)

            if decision == 1:
                mapped_grn.append(u_g)
                mapped_wsn.append(u_w)
                E.extend(e)

    # print len(directed),len(mapped_grn),len(mapped_wsn)
    return mapped_wsn,E,ppe,den


