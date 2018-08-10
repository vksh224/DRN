import csv
import networkx as nx
import re
from math import radians, cos, sin, asin, sqrt, inf
from degree import *

def funHaversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """

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


def readDatasets(shelterpoint_file, poi_file):
    site_ids = []
    site_coors = []
    site_zones = []

    with open(shelterpoint_file, 'r') as csvfile:
        SP_rows = csv.reader(csvfile, delimiter=',')

        line_count = 0
        for row in SP_rows:
            # Ignore first two rows
            if line_count < 2:
                line_count += 1
            else:

                site_zones.append(row[9])
                if row[9] == "Bagmati" or 1 == 1:
                    site_ids.append(row[0])
                    site_coors.append((row[13], row[14]))

    with open(poi_file, 'r') as csvfile:
        poi_rows = csv.reader(csvfile, delimiter=',')

        count_notSchools = 0
        for row in poi_rows:
            if row[2] != "school" and row[2]!= "college":
                patternMatch = re.match(r'^Polygon \(\((.*)\)\)', row[0], re.M | re.I)
                if patternMatch:
                    #print ("Pattern 1: ", patternMatch.group(1))
                    selected_coordinate = patternMatch.group(1).split(",")[0]
                    #print ("Coor: ", selected_coordinate)
                    x_coor = selected_coordinate.split(" ")[0]
                    y_coor = selected_coordinate.split(" ")[1]
                    #print("X Y", x_coor, y_coor)
                    site_ids.append(row[1])
                    site_coors.append((x_coor, y_coor))

                count_notSchools += 1

        print("Not schools: ", count_notSchools)

    return site_ids, site_coors, site_zones



def create_static_network(shelterpoint_file, poi_file):
    wifi_range = 5000

    site_ids, site_coors, site_zones = readDatasets(shelterpoint_file, poi_file)

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

G = create_static_network('NepalEarthquakeR4.csv', "KTM_POIs.csv")
nx.write_gml(G, "inputDRN.gml")
deg(G)



