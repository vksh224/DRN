#from writer import *
from inputs import *
from numpy import linalg as LA

import pickle
import copy
import random
#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as plt

np.set_printoptions(suppress = True)
np.set_printoptions(precision = 6)

def plot_graph(G, filename):
    plt.figure()
    plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())))
    nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.draw()
    plt.savefig(filename + "_" + str(len(G.nodes())) + ".png")
    plt.close()

def plot_deg_dist(G, filename):
    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1

    plt.figure()
    plt.plot(X, Y)
    plt.savefig(filename + '_' + str(len(G.nodes())) + ".png")
    plt.close()

def supplement(GBD,G2,t1_G2):
    D = list(set(G2.nodes()) - set(GBD.nodes()))
    GBD.add_nodes_from(D)
    D.extend(nx.isolates(GBD))
    print("Isolated nodes:", len(D))

    for u in D:
        for v in t1_G2:
            if nx.has_path(G2,u,v):
                p = nx.shortest_path(G2,source = u,target = v)
                for i in range(1,len(p)):
                    GBD.add_edge(p[i - 1],p[i])
                break
    return GBD

def prep(_hG,_sG,_nG,hD,sD,nD,sim,mNO):

    hFG = []
    sFG = []
    nFG = []

    hFD = []
    sFD = []
    nFD = []

    outer = False
    mapped = 0
    sim = np.array(sim)
    for i in range(len(sim)):
        for j in range(len(sim)):

            pos = np.argwhere(np.amax(sim) == sim)
            #print pos,mapped
            #input('hi')
            uG = pos[0][0]
            uD = pos[0][1]
            flag = 0
            if mNO[uG] in _hG and uD in hD:
                hFG.append(mNO[uG])
                hFD.append(uD)
                flag = 1

            elif mNO[uG] in _sG and uD in sD:
                sFG.append(mNO[uG])
                sFD.append(uD)
                flag = 1

            elif mNO[uG] in _nG and uD in nD:
                nFG.append(mNO[uG])
                nFD.append(uD)
                flag = 1

            if flag == 1:
                sim[uG,:] = [-1.0 for i in range(len(sim))]
                sim[:,uD] = [-1.0 for i in range(len(sim))]

                mapped += 1

            sim[uG,uD] = -1.0

            if mapped >= len(sim):
                outer = True
                break

        if outer:
            break
    return hFG,sFG,nFG,hFD,sFD,nFD


def check(A,B,e):

    for eachA in range(len(A)):
        for eachB in range(len(A[0])):
            if abs(A[eachA][eachB] - B[eachA][eachB]) > e:
                return False

    return True


def similarity(G1,G2):

    #G1 = nx.gnp_random_graph(10,p = 0.4,directed = True)
    #G2 = nx.gnp_random_graph(10,p = 0.3,directed = True)

    #print (len(G1))
    #print (len(G2))

    inG1 = [G1.predecessors(u) for u in G1.nodes()]
    inG2 = [G2.predecessors(u) for u in G2.nodes()]

    outG1 = [G1.successors(u) for u in G1.nodes()]
    outG2 = [G2.successors(u) for u in G2.nodes()]

    #print (inG1)
    #print (inG2)
    #print (outG1)
    #print (outG2)

    oS = [[-1.0 for i in range(len(G2))] for j in range(len(G1))]
    S = [[0.1 for i in range(len(G2))] for j in range(len(G1))]
    #print (S)
    e = 0.00001
    Iterate = 10000
    counter = 0

    while(counter < Iterate):

        #print (counter)
        _S = [[0.0 for i in range(len(G2))] for j in range(len(G1))]
        for i in G1.nodes():

            for j in G2.nodes():
                if len(outG1[i]) == 0 or len(outG2[j]) == 0:
                    continue

                for p in outG1[i]:
                    for q in outG2[j]:
                        _S[i][j] += S[p][q]

        for i in G1.nodes():
            for j in G2.nodes():

                if len(inG1[i]) == 0 or len(inG2[j]) == 0:
                    continue

                for p in inG1[i]:
                    for q in inG2[j]:
                        _S[i][j] += S[p][q]


        #f = lambda x: x
        #sq = np.sum([[f(_S[u][v]) for v in range(len(_S[0]))] for u in range(len(_S))])

        PSD = B = np.dot(_S,np.transpose(_S))
        w,v = LA.eig(PSD)
        sq = math.sqrt(max(w))

        _S = [[float(_S[j][i])/float(sq) for i in range(len(G2))] for j in range(len(G1))]

        if check(S,_S,e) or check(oS,_S,e):
            return S

        oS = copy.copy(S)
        S = copy.copy(_S)
        #print (np.array(S))
        counter += 1

def dist(u, v):
    d = 0.0
    for i in range(len(u)):
        d = d + math.pow((u[i] - v[i]), 2)

    return math.sqrt(d)

def mapping(hD,sD,nD,hG,sG,nG):

    #One to one mapping: DRN --> GRN
    m = {}
    for i in range(len(hD)):
        m[hD[i]] = hG[i]

    for i in range(len(sD)):
        m[sD[i]] = sG[i]

    for i in range(len(nD)):
        m[nD[i]] = nG[i]

    return m

def create(n,Coor,TRan):

    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(n)])
    for u in G.nodes():
        for v in G.nodes():

            if u == v:
                continue

            if dist(Coor[u], Coor[v]) <= TRan:
                #r = random.randint(0, 2)
                #if r == 0:
                    #G.add_edge(u, v)
                #if r == 1:
                    #G.add_edge(v, u)
                #else:
                G.add_edge(u, v)
                G.add_edge(v, u)



    return G

def place(Xlim, Ylim, TRan, N):

    G = nx.DiGraph()
    G.add_nodes_from([u for u in range(N)])

    Coor = []

    for i in range(N):
        x = random.uniform(0, Xlim)
        y = random.uniform(0, Ylim)

        Coor.append([x, y])

    print (Coor)
    #plt.scatter([pt[0] for pt in Coor], [pt[1] for pt in Coor], s=3, c='blue')
    #plt.show()

    G = create(N,Coor,TRan)

    return G, Coor

def correctness(gG,test,m):
#Checking Correctness

    for e in test.edges():
        try:
            if not nx.has_path(gG,m[e[0]],m[e[1]]):
                return False
        except:
            continue

    return True

def mapToGRN(rG,gD,hG,sG,nG,hD,sD,nD):

    mgD = nx.DiGraph()
    mgD.add_nodes_from(gD.nodes())
    for e in gD.edges():

        try:
            if e[0] in hD and e[1] in sD:
                u = hD.index(e[0])
                v = sD.index(e[1])
                if nx.has_path(rG,hG[u],sG[v]):
                    mgD.add_edge(e[0],e[1])

            elif e[0] in hD and e[1] in nD:
                u = hD.index(e[0])
                v = nD.index(e[1])
                if nx.has_path(rG,hG[u],nG[v]):
                    mgD.add_edge(e[0],e[1])


            elif e[0] in sD and e[1] in sD:
                if e[0] == e[1]:
                    continue

                u = sD.index(e[0])
                v = sD.index(e[1])
                if nx.has_path(rG,sG[u],sG[v]):
                    mgD.add_edge(e[0],e[1])


            elif e[0] in sD and e[1] in nD:
                u = sD.index(e[0])
                v = nD.index(e[1])
                if nx.has_path(rG,sG[u],nG[v]):
                    mgD.add_edge(e[0],e[1])

        except:
            continue

    return mgD

def refGRN(G,rH,rS,rN,hCount,sCount,nCount,kh,kn,mC):

    rG = nx.DiGraph()

    rG.add_nodes_from(rS[:sCount])
    #print "This:",[mC[i] for i in rS[:sCount]]
    hubFlag = False

    toBeMapped = rH + rN
    mapCount = 0

    for node in toBeMapped:

        count = 0
        for exist in rG.nodes():

            if not hubFlag:
                if G.has_edge(node, exist) or G.has_edge(exist, node):
                    count += 1
            elif G.has_edge(exist, node):
                count += 1

            if not hubFlag and count >= kh:
                break
            if count >= kn:
                break
        if not hubFlag and count >= kh:
            rG.add_node(node)
            mapCount += 1
        elif count >= kn:
            rG.add_node(node)
            mapCount += 1

            #print mapCount

        if mapCount >= hCount and not hubFlag:
            toBeMapped = toBeMapped[len(rH):]
            mapCount = 0
            hubFlag = True
            continue

        elif mapCount >= nCount and hubFlag:
            break

    for e in G.edges():
        if e[0] in rG.nodes() and e[1] in rG.nodes():
            rG.add_edge(e[0],e[1])

    return rG

def reassign(r,hD,sD,nD,gD,Coor,Xlim,Ylim):

    #print "gD:",gD
    for i in range(int(r)):

        u = random.choice(nD)

        x = random.uniform(0,Xlim)
        y = random.uniform(0,Ylim)
        Coor[u] = (x,y)


    return hD,sD,nD,Coor

def saver(fileG,fileR,mgD,gD,m,cnt,Coor):


    for u in gD.nodes():

        s = str(cnt * 3600) + ' ' + str(u) + ' ' + str(Coor[u][0]) + ' ' + str(Coor[u][1])
        with open(fileR, "a") as myfile:
            myfile.write(s)
            myfile.write('\n')

    for u in mgD.nodes():
        s = str(cnt * 3600) + ' ' + str(u) + ' ' + str(Coor[u][0]) + ' ' + str(Coor[u][1])
        with open(fileG, "a") as myfile:
            myfile.write(s)
            myfile.write('\n')

def findSinks(G,D,K,t,gSink,dSink):


    allcontenders = [G.out_degree(u) for u in G.nodes()]
    contenders = sorted(range(len(allcontenders)), key = lambda x: allcontenders[x])
    contenders = contenders[- int(K):]
    contenders = [allcontenders[each] for each in contenders]
    print (contenders)

    with open(gSink, "a") as myfile:
        myfile.write(str(contenders) + '\n')


    contenders = [D.out_degree(u) for u in D.nodes()]
    contenders = sorted(range(len(contenders)), key = lambda x: contenders[x])
    contenders = contenders[- int(K):]

    #print contenders

    with open(dSink, "a") as myfile:
        myfile.write(str(contenders) + '\n')


def mCount(mList,G,hG, sG, nG):

    '''
    G = G.to_undirected()
    mList = []
    for i in G.nodes():
        #print (i)
        for j in G.nodes():
            if j <= i:
                continue
            for k in G.nodes():
                if k <= j:
                    continue

                if G.has_edge(i,j) and G.has_edge(j,k) and G.has_edge(i,k):
                    mList.append([i,j,k])


    '''
    C = [0.0 for i in range(len(G))]
    for motif in mList:
        for node in motif:
            C[node] += 1.0

    rankList = sorted(range(len(C)), key = lambda x: C[x])[::-1]

    rH = [i for i in rankList if i in hG]
    rS = [i for i in rankList if i in sG]
    rN = [i for i in rankList if i in nG]

    return C,rankList,rH,rS,rN

def tiers(G):

    hub = []
    sub = []
    non = []
    for i in G.nodes():

        if G.out_degree(i) == 0:
            non.append(i)
        elif G.in_degree(i) == 0:
            hub.append(i)
        else:
            sub.append(i)

    return hub,sub,non

def place(Xlim, Ylim, TRan, N):

    G = nx.DiGraph()
    G.add_nodes_from([u for u in range(N)])

    Coor = []

    for i in range(N):
        x = random.uniform(0, Xlim)
        y = random.uniform(0, Ylim)

        Coor.append([x, y])

    #print Coor
    #plt.scatter([pt[0] for pt in Coor], [pt[1] for pt in Coor], s=3, c='blue')
    #plt.show()

    G = create(N,Coor,TRan)

    return G, Coor


#Main starts here
isFirst = True
hD = []
sD = []
nD = []
cnt = -1

#fileR = str(ND) + 'R.txt'
#fileG = str(ND) + 'G.txt'

yeast_directory = "../Yeast_Data/"
data_directory = '../Bhaktapur/Data/'
gG = nx.read_gml(yeast_directory + 'Yeast_Ordered.gml')
gG = nx.convert_node_labels_to_integers(gG)
#print "Number of nodes in GRN graph:",len(gG)
#print "Number of edges in GRN graph:",len(gG.edges())
hG , sG, nG = tiers(gG)
#print len(nG),len(sG),len(hG)


#Count motif list and motif centrality in GRN graph gG
mList = pickle.load( open(yeast_directory + "Motif_Yeast.p", "rb" ) )
#mList = []
mC,rmC,hG,sG,nG = mCount(mList,gG,hG,sG,nG)
#print (mList)

#pickle.dump(mList, open( "mList.p", "wb" ))
print (len(hG))

'''
gD,coor = place(Xlim,Ylim,TRan,ND)

# Distribution of hub, sub and non nodes in DRN graph gD
hCount = int(hR * float(ND))
sCount = int(sR * float(ND))
nCount = ND - hCount - sCount

# List of hub, sub and non nodes in DRN graph gD and GRN graph gG
hD = [i for i in range(hCount)]
sD = [(i + hCount) for i in range(sCount)]
nD = [(i + hCount + sCount) for i in range(nCount)]
'''

gD = nx.read_gml('../Bhaktapur/Orig_NepalDRN_0.gml')
coor = pickle.load(open('../Bhaktapur/Data/CC_locs.p', 'rb'))
coor.append(pickle.load(open('../Bhaktapur/Data/PoI_locs.p', 'rb')))
coor.append(pickle.load(open('../Bhaktapur/Data/Vol_locs.p', 'rb')))
coor.append(pickle.load(open('../Bhaktapur/Data/S_locs.p', 'rb')))

plot_deg_dist(gD, 'Plots/Orig_NepalDRN_degree')
plot_graph(gD, "Plots/Orig_NepalDRN")

print("Number of nodes in DRN graph:", len(gD))
print("Number of edges in DRN graph:", len(gD.edges()))
print("Density: ", (float(len(gD.edges()))/ (len(gD) * (len(gD) - 1))))

hD = pickle.load(open(data_directory + "HO.p", "rb" ))
sD = pickle.load(open(data_directory + "SO.p", "rb" ))
nD = pickle.load(open(data_directory + "NO.p", "rb" ))

hCount = len(hD)
sCount = len(sD)
nCount = len(nD)

print("hD", hD, sD)

# Find reference GRN
rG = refGRN(gG, hG, sG, nG, hCount, sCount, nCount, kh, kn, mC)
#print "Number of nodes in Reference GRN graph:", len(rG)
#print "Number of edges in Reference GRN graph:", len(rG.edges())

_rG = nx.convert_node_labels_to_integers(rG, first_label=0, label_attribute='old_label')

mNO = {}
mON = {}
for u in _rG.nodes():
    v = _rG.node[u]['old_label']
    mNO[u] = v
    mON[v] = u

sim = similarity(_rG, gD)

_hG, _sG, _nG, hD, sD, nD = prep(hG[:hCount], sG[:sCount], nG[:nCount], hD, sD, nD, sim, mNO)

mgD = mapToGRN(rG, gD, _hG, _sG, _nG, hD, sD, nD)

print("Number of nodes in BIO-DRN graph:", len(mgD))
print("Number of edges in BIO-DRN graph:", len(mgD.edges()))
print("Is Bio-DRN connected?", nx.is_connected(mgD.to_undirected()))
#print("Largest connected component", len(list(nx.connected_component_subgraphs(mgD.to_undirected()))))

plot_deg_dist(mgD, 'Plots/notFinal_bio_degree')
plot_graph(mgD, "Plots/notFinal_bio")

mgD = supplement(mgD, gD, hD)
print ("FINAL NODE COUNT:", len(mgD))
print ("FINAL EDGE COUNT:", len(mgD.edges()))
print("Is Bio-DRN connected after supplementary step?", nx.is_connected(mgD.to_undirected()))

#print(mgD.nodes())

plot_deg_dist(mgD, 'Plots/bio_final_degree')
plot_graph(mgD, "Plots/bio_final")

'''
while(True):

    if cnt >= iter:
        break

    cnt += 1

    if isFirst:
        gD,coor = place(Xlim,Ylim,TRan,ND)
        isFirst = False

    else:
        hD,sD,nD,coor = reassign(r,hD,sD,nD,gD,coor,Xlim,Ylim)
        gD = create(ND,coor,TRan)


    #gD = nx.erdos_renyi_graph(ND, p, seed=None, directed = True)
    #gD = nx.convert_node_labels_to_integers(gD,first_label = 0)
    print "Number of nodes in DRN graph:",len(gD)
    print "Number of edges in DRN graph:",len(gD.edges())

    #Distribution of hub, sub and non nodes in DRN graph gD
    hCount = int(hR * float(ND))
    sCount = int(sR * float(ND))
    nCount = ND - hCount - sCount

    #List of hub, sub and non nodes in DRN graph gD and GRN graph gG
    hD = [i for i in range(hCount)]
    sD = [(i + hCount) for i in range(sCount)]
    nD = [(i + hCount + sCount) for i in range(nCount)]
    #print "Number of hub, sub and non nodes in DRN graph gD",len(hD),len(sD),len(nD)
    #print "Number of hub, sub and non nodes in GRN graph gD",len(hG),len(sG), len(nG)

    #Find reference GRN
    rG = refGRN(gG,hG,sG,nG,hCount,sCount,nCount,kh,kn,mC)
    print "Number of nodes in Reference GRN graph:",len(rG)
    print "Number of edges in Reference GRN graph:",len(rG.edges())


    _rG = nx.convert_node_labels_to_integers(rG,first_label = 0,label_attribute = 'old_label')

    mNO = {}
    mON = {}
    for u in _rG.nodes():
        v = _rG.node[u]['old_label']
        mNO[u] = v
        mON[v] = u

    sim = similarity(_rG,gD)

    _hG,_sG,_nG,hD,sD,nD = prep(hG[:hCount],sG[:sCount],nG[:nCount],hD,sD,nD,sim,mNO)

    mgD = mapToGRN(rG,gD,_hG,_sG,_nG,hD,sD,nD)
    print "Number of nodes in BIO-DRN graph:",len(mgD)
    print "Number of edges in BIO-DRN graph:",len(mgD.edges())

    m = mapping(hD,sD,nD,_hG,_sG,_nG)
    print m
    print ("THIS IS:",str([mgD.out_degree(mON[each]) for each in _hG]))

    if not correctness(gG,mgD,m):
        print "ALARM!"
    else:
        print "WELL MAPPED!"

    neighbor(gD,mgD,m,hD,cnt)
    writers(gD,coor,cnt)
    #fname_o = str(ND) + 'o.gml'
    #nx.write_gml(gD,fname_o)

    #fname_m = str(ND) + 'm.gml'
    #nx.write_gml(mgD,fname_m)

    #input('check')
    #findSinks(mgD,gD,sink,cnt,gsink,dsink)

    #E = set(gD.edges())  # optimization
    #G_st = nx.DiGraph()
    #G_st.add_edges_from([e for e in gD.edges() if e in E])
    G_st = nx.minimum_spanning_tree(gD.to_undirected())

    s_st = ''
    for u in G_st.nodes():
        s_st += str(cnt * 600) + ' ' + str(u)

        for v in G_st.neighbors(u):
            if v < u:
                s_st += ' ' + str(v)
        s_st += '\n'

    f_st = str(len(gD)) + '_st.txt'
    with open(f_st, "a") as myfile:
        myfile.write(s_st)


    G_os = gD.copy()
    diff = len(gD.edges()) - len(mgD.edges())
    for i in range(diff):
        e = random.choice(G_os.edges())
        G_os.remove_edge(e[0],e[1])


    s_os = ''
    for u in G_os.nodes():
        s_os += str(cnt * 600) + ' ' + str(u)
        for v in G_os.successors(u):
            s_os += ' ' + str(v)

        s_os += '\n'

    f_os = str(len(gD)) + '_os.txt'
    with open(f_os, "a") as myfile:
        myfile.write(s_os)

'''
