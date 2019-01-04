import networkx as nx

directory = "Bhaktapur_1/4/"
data_directory = directory + "Data/"
t = 1800

O = nx.read_gml(directory + 'Orig_NepalDRN_' + str(t) + '.gml')
print("Orig nodes and edges:" , len(O.nodes()), len(O.edges()))

B = nx.read_gml(data_directory + 'Bio_' + str(t) + '.gml')
print("Bio nodes and edges:" , len(B.nodes()), len(B.edges()))

R = nx.read_gml(data_directory + 'Random_' + str(t) + '.gml')
print("Random nodes and edges:" , len(R.nodes()), len(R.edges()))

S = nx.read_gml(data_directory + 'Spanning_' + str(t) + '.gml')
print("Spanning nodes and edges:" , len(S.nodes()), len(S.edges()))

K2 = nx.read_gml(data_directory + 'K2_' + str(t) + '.gml')
print("K2 nodes and edges:" , len(K2.nodes()), len(K2.edges()))

K4 = nx.read_gml(data_directory + 'K4_' + str(t) + '.gml')
print("K4 nodes and edges:" , len(K4.nodes()), len(K4.edges()))

K8 = nx.read_gml(data_directory + 'K8_' + str(t) + '.gml')
print("K8 nodes and edges:" , len(K8.nodes()), len(K8.edges()))