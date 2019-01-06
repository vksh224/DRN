import networkx as nx
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

def convert_to_string(l):
    s = ''
    for i in range(len(l)):
        s = s + str(l[i]) + ' '

    return s

def write_to_file(L,fname):

    s = 'time #perc. #Orig #Bio #R #K2 #K8 #S \n'
    f = open(fname,'w')
    f.write(s)

    L = np.array(L)
    t = 1
    p = 2

    for i in range(L.shape[1]):
        l = list(L[:,i])
        print (l)

        s = convert_to_string(l)
        s = str(t) + ' ' + str(p * t) + ' ' + s + '\n'
        f.write(s)

        t = t + 1

    f.close()


def aggregate(L):

    M = []
    for i in range(len(L)):
        M.append(np.average(L[i]))

    return M

def failed_gen(r):

    f = [[]]
    for l in r[1:]:
        current = [int(u) for u in l.split()[1:]]
        f.append(current)

    return f

def rename_graph(O):

    m = {}
    for u in O.nodes():
        m[u] = int(u)

    O = nx.relabel_nodes(O,m)
    return O

def pathcount(G,CC,S):

    #print (len(G),len(G.edges()))
    #print G.nodes()

    p = 0.0
    for s in S:
        if s not in G.nodes():
            continue
        for c in CC:
            if c not in G.nodes():
                continue

            if nx.has_path(G,s,c):
                paths = nx.all_simple_paths(G, source = s, target = c,cutoff = 4)
                p += len(list(paths))
    return p

def efficiency(G,CC,S):
    e = 0.0
    den = 0.0
    for s in S:
        if s not in G.nodes():
            continue

        for c in CC:
            if c not in G.nodes():
                continue

            if nx.has_path(G, s, c):
                l = nx.shortest_path_length(G, source = s, target = c)
                e = e + 1.0/float(l)

            den = den + 1.0

    if den == 0:
        return 0

    return float(e)/den

def motif(G):
    m = 0


    for u in G.nodes():
        for v in G.nodes():
            if v <= u:
                continue

            for w in G.nodes():
                if w <= v:
                    continue

                if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                    m += 1


    #return len(nx.triangles(G))
    return m

#modes: 0: efficiency, 1:pathcount, 2: motif
mode = 2
option = 1 #which 0 - for 3 Pois, 1 - for 5 pois, 2 for 7 pois
how_many_instances = 1
how_many_timeslots = 10

root_directory = '/Users/vijay/DRN_Project/'
#path_source_files = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur_0/'
#path_source_files = '/localdisk2/SCRATCH/DRN_Project/Bhaktapur_1/'
path_source_files = root_directory + 'Bhaktapur_' + str(option) + '/'

#failed_node_list = '/localdisk2/SCRATCH/BioDRN_ONE/BioDRN/src/FailedNodeList/1_10/'
os.chdir(path_source_files)

O_List = [[] for _ in range(how_many_timeslots)]
B_List = [[] for _ in range(how_many_timeslots)]
R_List = [[] for _ in range(how_many_timeslots)]
K2_List = [[] for _ in range(how_many_timeslots)]
K4_List = [[] for _ in range(how_many_timeslots)]
K8_List = [[] for _ in range(how_many_timeslots)]
s_List = [[] for _ in range(how_many_timeslots)]

for i in [0,1,2]:

    os.chdir(str(i) + '/Data/')

    # Read files
    CC = pickle.load(open('CC_locs.p','rb'))
    PoI = pickle.load(open('PoI_locs.p','rb'))
    Vol = pickle.load(open('Vol_locs.p','rb'))
    S = pickle.load(open('S_locs.p','rb'))

    Res_paths = pickle.load(open("Res_paths.p", "rb"))

    # This is not consistent with V from other files. Here, it includes the responders too
    V = len(CC) + len(PoI) + len(Vol) + len(S) + len(Res_paths)

    # Find source destination nodes
    CC_IDs = range(len(CC))
    PoI_IDs = range(len(CC), len(CC) + len(PoI))
    Vol_IDs = range(len(CC) + len(PoI), len(CC) + len(PoI) + len(Vol))
    S_IDs = range(len(CC) + len(PoI) + len(Vol),len(CC) + len(PoI) + len(Vol) + len(S))

    #failed_node_list = '/Users/satyakiroy/PycharmProjects/DRN_Project/FailedNodeList/0_' + str(i) + '/'
    failed_node_list = root_directory + 'FailedNodeList/' + str(option) + '_' + str(i) + '/'

    #Failed nodelist
    F = open(failed_node_list + 'failed_nodelist_' + str(V) + '.txt','r')
    r = F.readlines()
    f = failed_gen(r)

    t = 0

    #Read topologies
    O = nx.read_gml('../Orig_NepalDRN_' + str(t) + '.gml')
    O = rename_graph(O)

    B = nx.read_gml('Bio_' + str(t) + '.gml')
    B = rename_graph(B)
    print("B: Nodes and edges:", len(B.nodes()), len(B.edges()), "is_connected", nx.is_connected(B))

    R = nx.read_gml('Random_' + str(t) + '.gml')
    R = rename_graph(R)
    print("R: Nodes and edges:", len(R.nodes()), len(R.edges()), "is_connected", nx.is_connected(R))

    K2 = nx.read_gml('K2_' + str(t) + '.gml')
    K2 = rename_graph(K2)
    print("K2: Nodes and edges:", len(K2.nodes()), len(K2.edges()), "is_connected", nx.is_connected(K2))

    K4 = nx.read_gml('K4_' + str(t) + '.gml')
    K4 = rename_graph(K4)
    print("K4: Nodes and edges:", len(K4.nodes()), len(K4.edges()), "is_connected", nx.is_connected(K4))

    K8 = nx.read_gml('k8_' + str(t) + '.gml')
    K8 = rename_graph(K8)
    print("K8: Nodes and edges:", len(K8.nodes()), len(K8.edges()), "is_connected", nx.is_connected(K8))

    s = nx.read_gml('Spanning_' + str(t) + '.gml')
    s = rename_graph(s)
    print("ST: Nodes and edges:", len(s.nodes()), len(s.edges()), "is_connected", nx.is_connected(s))

    #print (O.nodes())
    #print PoI_IDs

    for j in range(1,len(f)):

        print (list(set(f[j]) - set(f[j - 1])))

        O.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        B.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        R.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K2.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K4.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K8.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        s.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))

        O.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        B.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        R.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K2.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K4.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K8.add_nodes_from(list(set(f[j]) - set(f[j - 1])))
        s.add_nodes_from(list(set(f[j]) - set(f[j - 1])))

        #print motif(O)
        #print motif(B)
        #print motif(K2)
        #print motif(K4)
        #print motif(s)

        if mode == 0:
            O_List[j - 1].append(efficiency(O, CC_IDs, S_IDs))
            B_List[j - 1].append(efficiency(B, CC_IDs, S_IDs))
            R_List[j - 1].append(efficiency(R, CC_IDs, S_IDs))
            K2_List[j - 1].append(efficiency(K2, CC_IDs, S_IDs))
            K4_List[j - 1].append(efficiency(K4, CC_IDs, S_IDs))
            K8_List[j - 1].append(efficiency(K8, CC_IDs, S_IDs))
            s_List[j - 1].append(efficiency(s, CC_IDs, S_IDs))

        elif mode == 1:
            O_List[j - 1].append(pathcount(O,CC_IDs,S_IDs))
            B_List[j - 1].append(pathcount(B,CC_IDs,S_IDs))
            R_List[j - 1].append(pathcount(R,CC_IDs,S_IDs))
            K2_List[j - 1].append(pathcount(K2,CC_IDs,S_IDs))
            K4_List[j - 1].append(pathcount(K4, CC_IDs, S_IDs))
            K8_List[j - 1].append(pathcount(K8,CC_IDs,S_IDs))
            s_List[j - 1].append(pathcount(s,CC_IDs,S_IDs))
        else:
            O_List[j - 1].append(motif(O))
            B_List[j - 1].append(motif(B))
            R_List[j - 1].append(motif(R))
            K2_List[j - 1].append(motif(K2))
            K4_List[j - 1].append(motif(K4))
            K8_List[j - 1].append(motif(K8))
            s_List[j - 1].append(motif(s))


        #input('')

    os.chdir(path_source_files)

O_List = aggregate(O_List)
B_List = aggregate(B_List)
R_List = aggregate(R_List)
K2_List = aggregate(K2_List)
K4_List = aggregate(K4_List)
K8_List = aggregate(K8_List)
s_List = aggregate(s_List)

#print (O_List)
#print (B_List)
#print (R_List)
#print (K2_List)
#print (K4_List)
#print (s_List)


timeslot_duration = 1800.0
L = [O_List,B_List,R_List,K2_List,K8_List,s_List]
#os.chdir('/Users/satyakiroy/PycharmProjects/DRN_Project')
os.chdir(root_directory)

if mode == 0:
    write_to_file(L, root_directory + 'Graph_Experiments/' + str(option) + '/NE.txt')

elif mode == 1:
    write_to_file(L, root_directory + 'Graph_Experiments/' + str(option) +  '/path.txt')

else:
    write_to_file(L, root_directory + 'Graph_Experiments/' + str(option) + '/motif.txt')

'''
#Visualization
colorlist = ['r','g','b','black','magenta','purple']

for i in range(len(L)):
    plt.plot([j for j in range(len(L[i]))],L[i],marker = 'o',color = colorlist[i])

plt.xticks([j for j in range(len(L[i]))],[j * timeslot_duration for j in range(len(L[i]))])
plt.show()
'''
