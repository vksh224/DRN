import networkx as nx
from embedding import *


fidelity = 0.8

#Read GRN
GRN = nx.read_gml('this_grn.gml')
#GRN = GRN.reverse()
GRN = nx.convert_node_labels_to_integers(GRN,first_label = 0)

DRN = nx.read_gml('inputDRN.gml')
DRN = nx.convert_node_labels_to_integers(DRN,first_label = 0)

print("\nNumber of nodes in GRN: ", len(GRN))
print("Number of edges in GRN: ", len(GRN.edges()))

#Calculate rank vectors
r_g = nx.pagerank(GRN)
r_w = nx.pagerank(DRN)

#Mapped graph
MW,E,_,_ = embed_map(GRN,DRN,r_g,r_w,fidelity)

MW_graph = nx.Graph()
MW_graph.add_nodes_from(MW)
MW_graph.add_edges_from(E)

print ("MappedDRN: Nodes ", len(MW))
print ("MappedDRN: Edges ", len(E))
print("MappedDRN: is connected ", nx.is_connected(MW_graph))
print("MappedDRN: No. of triangles ", len(nx.triangles(MW_graph)))
# plot_graph(MW_graph, "MW", fidelity)

