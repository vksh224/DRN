import csv
import networkx as nx
from math import radians, cos, sin, asin, sqrt, inf
from degree import *

def funHaversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #print("lon1: " + str(lon1) + " lat1: " + str(lat1) + " lon2: " + str(lon2) + " lat2: " + str(lat2) )

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371* c * 1000
    # print(" dist: " + str(km))
    return m



def create_static_network(filename):
    wifi_range = 25000

    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')

        site_ids = []
        site_coors = []
        site_zones = []

        line_count = 0
        for row in rows:
            # Ignore first two rows
            if line_count < 2:
                line_count += 1
            else:

                site_zones.append(row[9])
                if row[9] == "Bagmati" or 1 == 1:
                    site_ids.append(row[0])
                    site_coors.append((row[13], row[14]))

    # Initialize graph
    G = nx.Graph()

    # add nodes
    for i in range(len(site_ids)):
        G.add_node(site_ids[i])

    #add edges
    for i in range(len(site_ids)):
        u = site_ids[i]
        lat1 = site_coors[i][0]
        lon1 = site_coors[i][1]

        for j in range(len(site_ids)):
            v = site_ids[j]
            lat2 = site_coors[j][0]
            lon2 = site_coors[j][1]

            dist = funHaversine(float(lon1), float(lat1), float(lon2), float(lat2))

            if dist <= wifi_range:
                G.add_edge(u, v)

    print ("Number of nodes in G: ",len(G))
    print ("Number of edges in G: ",len(G.edges()))
    print ("Density of G: ",(2 * len(G.edges()))/(len(G) * (len(G) - 1)))

    return G

G = create_static_network('NepalEarthquakeR4.csv')
deg(G)



