import csv
import networkx as nx
import re
from math import radians, cos, sin, asin, sqrt, fsum
from degree import *
#from read_graph import plot_graph

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
    m = 6371 * c * 1000
    # print(" dist: " + str(km))
    return m

def centroid(points):
    x_coords = [float(p[0]) for p in points]
    y_coords = [float(p[1]) for p in points]
    _len = len(points)
    centroid_x = fsum(x_coords)/_len
    centroid_y = fsum(y_coords)/_len
    return (centroid_x, centroid_y)


def farthest_nodes_from_centroid(site_coors, centroid):
    max_dist = -1
    for i in range(len(site_coors)):
        lat1 = site_coors[i][0]
        lon1 = site_coors[i][1]
        dist = funHaversine(float(lon1), float(lat1), float(centroid[1]), float(centroid[0]))
        if dist > max_dist:
            max_dist = dist

    # print(max_dist)
    return int(max_dist / 1000)

def farthest_nodes(site_coors):
    max_dist = -1
    for i in range(len(site_coors)):
        lat1 = site_coors[i][0]
        lon1 = site_coors[i][1]

        for j in range(len(site_coors)):
            lat2 = site_coors[j][0]
            lon2 = site_coors[j][1]

            dist = funHaversine(float(lon1), float(lat1), float(lon2), float(lat2))

            if dist > max_dist:
                max_dist = dist

    #print(max_dist)
    return int(max_dist/1000)


def readDatasets(shelterpoint_file, poi_file):
    site_ids = []
    site_coors = []
    site_zones = []
    SP_coors = []
    POI_coors = []
    POI_ids = []
    POI_types = []

    with open(shelterpoint_file, 'r') as csvfile:
        SP_rows = csv.reader(csvfile, delimiter=',')

        line_count = 0
        for row in SP_rows:
            # Ignore first two rows
            if line_count < 2:
                line_count += 1

            else:
                site_zones.append(row[9])
                if row[9] == "Bagmati":
                    site_ids.append(row[0])
                    site_coors.append((row[13], row[14]))
                    SP_coors.append((row[13], row[14]))

    SP_centroid = centroid(SP_coors)
    print("Centroid: ", SP_centroid)

    with open(poi_file, 'r') as csvfile:
        poi_rows = csv.reader(csvfile, delimiter=',')

        for row in poi_rows:
            patternMatch = re.match(r'^Polygon \(\((.*)\)\)', row[0], re.M | re.I)
            if patternMatch:
                #print ("Pattern 1: ", patternMatch.group(1))
                selected_coordinate = patternMatch.group(1).split(",")[0]
                #print ("Coor: ", selected_coordinate)
                x_coor = selected_coordinate.split(" ")[0]
                y_coor = selected_coordinate.split(" ")[1]

                #print("X Y", x_coor, y_coor)
                site_ids.append(row[1])
                POI_ids.append(row[1])
                site_coors.append((x_coor, y_coor))
                POI_coors.append((x_coor, y_coor))
                POI_types.append(row[2])

        #print("Not schools: ", count_notSchools)
    return POI_coors, POI_ids, POI_types


def filter_POIs(POI_coors, POI_ids, POI_types, farthest_distance):
    filtered_POI_coors = []
    filtered_POI_ids = []

    POI_centroid = centroid(POI_coors)
    print(POI_centroid)

    for ind in range(len(POI_coors)):
        if POI_types[ind] != "school" and POI_types[ind] != "college":
            dist = funHaversine(float(POI_coors[ind][1]), float(POI_coors[ind][0]), float(POI_centroid[1]), float(POI_centroid[0]))

            if dist <= farthest_distance:
                filtered_POI_coors.append(POI_coors[ind])
                filtered_POI_ids.append(POI_ids[ind])

    return filtered_POI_coors, filtered_POI_ids

def create_static_network(shelterpoint_file, poi_file):
    wifi_range = 700

    POI_coors, POI_ids, POI_types = readDatasets(shelterpoint_file, poi_file)
    POI_coors, POI_ids = filter_POIs(POI_coors, POI_ids, POI_types, 3000)

    # Initialize graph
    G = nx.Graph()

    # add nodes
    for i in range(len(POI_ids)):
        G.add_node(POI_ids[i])

    #add edges
    for i in range(len(POI_ids)):
        u = POI_ids[i]
        lat1 = POI_coors[i][0]
        lon1 = POI_coors[i][1]

        for j in range(len(POI_ids)):
            v = POI_ids[j]
            lat2 = POI_coors[j][0]
            lon2 = POI_coors[j][1]
            dist = funHaversine(float(lon1), float(lat1), float(lon2), float(lat2))
            if dist <= wifi_range:
                G.add_edge(u, v)

    print("Number of nodes in G: ",len(G))
    print("Number of edges in G: ",len(G.edges()))
    print("Density of G: ",(2 * len(G.edges()))/(len(G) * (len(G) - 1)))
    print("Is Connected:" , nx.is_connected(G), nx.number_connected_components(G))
    #print("Farthest shelter points:", farthest_nodes(SP_coors), "km")
    #print("Farthest shelter points from centroid:", farthest_nodes_from_centroid(SP_coors, SP_centroid), "km")
    print("Farthest POIs: ", farthest_nodes(POI_coors), "km")
    #print("Farthest Nodes: ", farthest_nodes(site_coors), "km")

    return G

folder = "kathmandu/"
G = create_static_network('kathmandu/NepalEarthquakeR4.csv', "kathmandu/KTM_POIs.csv")
nx.write_gml(G, folder + "inputDRN.gml")
#plot_graph(G, "inputDRN")



