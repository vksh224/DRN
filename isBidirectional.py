import os
import networkx as nx

#To check if any graph(s) is/are bidirectional.
#----------------------------------------------

def check_direction(G):

    for e in G.edges():
        if (e[1],e[0]) not in G.edges():
            return False

    return True

how_many = 3

for i in range(how_many):

    path = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur_0/' + str(i) + '/'
    os.chdir(path)


    G = nx.read_gml('Orig_NepalDRN_1800.gml')

    #print (len(G.nodes()))
    #print (len(G.edges()))

    print check_direction(G)

