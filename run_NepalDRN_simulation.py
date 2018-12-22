import os
import random
import networkx as nx
import pickle

no_of_PoI = 3

#option - high - More PoIs
for option in range(0,1):
    # no_of_PoI = count_PoI + random.randint(option, (2*option))
    no_of_PoI += 2
    for run in range(0, 3):
        root_directory = "Bhaktapur_" + str(option) + "/"
        directory = root_directory + str(run) + "/"

        # loc_des_folder = "/Users/vijay/BioDRN_ONE/BioDRN/src/NodePosition/" + str(option) + "_" + str(run) + "/"
        # neigh_des_folder = "/Users/vijay/BioDRN_ONE/BioDRN/src/NeighborList/" + str(option) + "_" + str(run) + "/"
        # setting_directory = "/Users/vijay/BioDRN_ONE/BioDRN/src/Nepal/" + str(option) + "_" + str(run) + "/"
        # failed_node_folder = "/Users/vijay/BioDRN_ONE/BioDRN/src/FailedNodeList/" + str(option) + "_" + str(run) + "/"
        # core_setting_directory = "/Users/vijay/BioDRN_ONE/BioDRN/src/Nepal/"

        #loc_des_folder = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/NodePosition/" + str(option) + "_" + str(run) + "/"
        #neigh_des_folder = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/NeighborList/" + str(option) + "_" + str(run) + "/"
        #setting_directory = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/Nepal/" + str(option) + "_" + str(run) + "/"
        #failed_node_folder = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/FailedNodeList/" + str(option) + "_" + str(run) + "/"
        #core_setting_directory = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/Nepal/"

        loc_des_folder = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/simulation/'
        neigh_des_folder = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/simulation/'
        setting_directory = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/simulation/'
        core_setting_directory = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/'
        failed_node_folder = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/simulation/'

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("root_directory" not in line) and \
                    ("directory" not in line) and \
                    ("loc_des_folder" not in line) and \
                    ("neigh_des_folder" not in line) and \
                    ("setting_directory" not in line) and \
                    ("core_setting_directory" not in line) and \
                    ("failed_node_folder" not in line) and \
                        ("no_of_PoI" not in line):

                    f.write(line)

            f.write("root_directory = '" + str(root_directory) + "'\n")
            f.write("directory = '" + str(directory) + "'\n")
            f.write("loc_des_folder = '" + str(loc_des_folder) + "'\n")
            f.write("neigh_des_folder = '" + str(neigh_des_folder) + "'\n")
            f.write("setting_directory = '" + str(setting_directory) + "'\n")
            f.write("core_setting_directory = '" + str(core_setting_directory) + "'\n")
            f.write("failed_node_folder = '" + str(failed_node_folder) + "'\n")
            f.write("no_of_PoI = " + str(no_of_PoI) + "\n")
            #f.write("max_S_in_PoI = " + str(max_S_in_PoI) + "\n")

        print("============ Option: " + str(option) + " Run: " + str(run) + " ============ ")

        #Place CC, Responders, and PoIs (and its survivors and volunteers) in the disaster area
        #os.system('python construct_Orig_NepalDRN.py')

        # Create Original DRN at each "network_construction_interval" until "total_simulation_time"
        #os.system('python construct_Orig_NepalDRN_network.py')

        # Create Bio-DRN corresponding to each "network_construction_interval" of Original DRN
        # os.system('python3 construct_Bio_NepalDRN.py')

        # Create other graph topologies, i.e., ST-DRN, Rand-DRN, K-DRN
        os.system('python genTop.py')

        #Create failed node list
        #os.system('python failed_nodelist.py' + directory)

        # Plot Orig and Bio-DRN degree distribution
        #os.system('python3 degree.py ')

        # Create ONE simulator setting file
        #os.system('python create_ONE_setting_new.py ' + str(option) + " " + str(run) + " " + directory)









'''
def generate_GRN_edge_directions_reversed(input_grn):
    G1 = nx.read_gml(input_grn)
    G1 = G1.reverse()
    G1 = nx.convert_node_labels_to_integers(G1,first_label = 0)
    nx.write_gml(G1, data_directory + 'yeast_grn_reversed.gml')
    return G1

def compute_GRN_NSM_NMC(G):
    # Node motif centrality
    NMC = {}
    # List of nodes sharing motif (NSM) with current node
    NSM = [[] for _ in G.nodes()]

    for u in G.nodes():
        NMC[u] = 0

    # For directed graphs
    if G.is_directed():
        for u in G.nodes():

            # print ("Node:",u)
            for v in G.nodes():
                for w in G.nodes():

                    if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

                        if v not in NSM[u]:
                            NSM[u].append(v)

                        if w not in NSM[u]:
                            NSM[u].append(w)

                        if u not in NSM[v]:
                            NSM[v].append(u)

                        if w not in NSM[v]:
                            NSM[v].append(w)

                        if u not in NSM[w]:
                            NSM[w].append(u)

                        if v not in NSM[w]:
                            NSM[w].append(v)

    # For undirected graphs
    else:
        for u in G.nodes():
            for v in G.nodes():
                if v <= u:
                    continue
                for w in G.nodes():
                    if w <= v:
                        continue

                    if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

    pickle.dump(NMC, open(data_directory + "NMC.p", "wb"))
    pickle.dump(NSM, open(data_directory + "NSM.p", "wb"))
    #return NMC, NSM
'''

#------------- Make GRN ready for mapping with DRN - to create Bio-DRN
# input GRN with edge directions reversed
#G = generate_GRN_edge_directions_reversed(input_grn)
#compute_GRN_NSM_NMC(G)
