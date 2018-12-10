import random
import math
import turtle
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from constants import *

def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
    return (math.sqrt((float(coor1X) - float(coor2X))**2 + (float(coor1Y) - float(coor2Y))**2))

def write_paths_to_a_file(Res_path_list, type):
    f = open(directory + 'responder_paths.txt', type)
    path_count = 1
    for res_path in Res_path_list:
        line_str = "Group.waypoints" + str(path_count) +" = "
        for coor in res_path:
            line_str += str(coor[0]) + ", " + str(coor[1]) + ", "
        f.write(line_str + "\n")
        path_count += 1
    f.close()

def get_responder_paths(CC_locs, PoI_locs):
    Res_path_list = []
    all_visited_pois = []

    rem_PoI_locs = [loc for loc in PoI_locs]
    for r in range(no_of_R):

        curr_res_path = []
        no_of_assigned_PoIs = random.randint(min_no_PoIs_for_R, max_no_PoI_for_R)
        curr_res_path.append(random.choice(CC_locs))

        for poi in range(no_of_assigned_PoIs):
            if len(rem_PoI_locs) == 0:
                rem_PoI_locs = [loc for loc in PoI_locs]

            if len(rem_PoI_locs) > 0:
                poi_loc = random.choice(rem_PoI_locs)
                curr_res_path.append(poi_loc)
                all_visited_pois.append(poi_loc)
                rem_PoI_locs.remove(poi_loc)

        Res_path_list.append(curr_res_path)

    print("Total unique PoIs served", len(set(all_visited_pois)), set(all_visited_pois))

    return Res_path_list

#---------------------------------- Survivor location --------------------------
def initial_survivor_loc(PoI_locs, PoI_radii, S_count_in_PoI):
    S_locs = []
    for i in range(len(PoI_locs)):
        for j in range(S_count_in_PoI[i]):
            # random angle
            alpha = 2 * math.pi * random.random()
            r = PoI_radii[i] * math.sqrt(random.random())
            # calculating coordinates
            x = r * math.cos(alpha) + PoI_locs[i][0]
            y = r * math.sin(alpha) + PoI_locs[i][1]
            S_locs.append((int(x), int(y)))
    return S_locs

def update_survivor_loc (PoI_locs, PoI_radii, S_locs, prev_time, curr_time):
    S_init_locs = pickle.load(open(directory + "Data/S_locs.p", "rb"))

    for i in range(len(S_locs)):
        moving_prob = random.uniform(0, 1)
        if moving_prob > moving_S_prob:
            # random angle
            alpha = 2 * math.pi * random.random()
            curr_speed = random.uniform (min_S_speed, max_S_speed)
            r = curr_speed * (curr_time - prev_time) * math.sqrt(random.random())

            x = -1
            y = -1
            #Check if a survivor belong to the current PoI
            for poi_ind in range(len(PoI_locs)):
                if euclideanDistance(S_init_locs[i][0], S_init_locs[i][1], PoI_locs[poi_ind][0], PoI_locs[poi_ind][1]) <= PoI_radii[poi_ind]:
                    x = max(S_locs[i][0] + r * math.cos(alpha), S_init_locs[i][0] + PoI_radii[poi_ind] * math.cos(alpha))
                    y = min(S_locs[i][1] + r * math.sin(alpha), S_init_locs[i][1] + PoI_radii[poi_ind] * math.sin(alpha))
                    print("Check: ", S_init_locs[i], PoI_locs[poi_ind], S_locs[i], x, y)
                    break

            S_locs[i] = (int(x), int(y))

    return S_locs
#-------------------End: Survivor related -------------------------------------


#------------ Volunteer path, initial location, and updated location -----------------------
def get_volunteer_paths(PoI_locs, PoI_radii, Vol_count_In_PoI):
    Vol_path_list = []
    for poi_id in range(len(PoI_locs)):
        for vol_id in range(Vol_count_In_PoI[poi_id]):
            polygon = turtle.Turtle()

            num_sides = random.randint(min_num_sides, max_num_sides)
            side_length = random.randint(min_side_length, max_side_length)
            angle = 360/ num_sides

            polygon.setposition(PoI_locs[poi_id])

            curr_vol_path = []
            #print("Number of sides: ", num_sides)
            for i in range(num_sides):
                # print(i, polygon.position())
                if euclideanDistance(PoI_locs[poi_id][0], PoI_locs[poi_id][1], polygon.position()[0], polygon.position()[1]) < PoI_radii[poi_id]:
                    curr_vol_path.append((int(polygon.position()[0]), int(polygon.position()[1])))
                polygon.forward(side_length)
                polygon.right(angle)

            Vol_path_list.append(curr_vol_path)

    return Vol_path_list

def initial_volunteer_loc(Vol_path_list):
    Vol_locs = []
    for path in Vol_path_list:
        Vol_locs.append(path[0])
    return Vol_locs

def update_volunteer_loc(Vol_locs, Vol_path_list, prev_time, curr_time):
    for i in range(len(Vol_locs)):
        curr_loc = Vol_locs[i]
        curr_speed = random.uniform(min_V_speed, max_V_speed)
        dist_trav = curr_speed * (curr_time - prev_time)
        pos = Vol_path_list[i].index(curr_loc)
        chosen_loc = curr_loc

        iteration = 0
        while True:
            pos = (pos + 1) % len(Vol_path_list[i])
            next_loc = Vol_path_list[i][pos]

            # if i == 0:
            #     print(i, "Curr loc", curr_loc, "Next loc", next_loc, Vol_path_list[i])
            #     print(euclideanDistance(next_loc[0], next_loc[1], curr_loc[0], curr_loc[1]), dist_trav)

            if iteration > len(Vol_path_list[i]):
                break

            if (euclideanDistance(next_loc[0], next_loc[1], curr_loc[0], curr_loc[1]) > dist_trav):
                Vol_locs[i] = chosen_loc
                break
            chosen_loc = next_loc
            iteration += 1
    return Vol_locs
#--------------------------------------------------------------------------------


def initial_setup():
    CC_locs = []
    PoI_locs = []
    PoI_radii = []
    Vol_count_In_PoI = []
    S_count_in_PoI = []

    #Get CC location
    for i in range(no_of_CC):
        CC_locs.append((random.randint(lX, hX), random.randint(lY, hY)))

    #Get PoI locations
    for i in range(no_of_PoI):
        PoI_locs.append((random.randint(lX, hX), random.randint(lY, hY)))
        PoI_radii.append(random.randint(min_PoI_radius, max_PoI_radius))
        Vol_count_In_PoI.append(random.randint(min_V_in_PoI, max_V_in_PoI))
        S_count_in_PoI.append(random.randint(min_S_in_PoI, max_S_in_PoI))

    #Get Responder paths
    Res_path_list = get_responder_paths(CC_locs, PoI_locs)

    #Get Volunteer paths
    Vol_path_list = get_volunteer_paths(PoI_locs, PoI_radii, Vol_count_In_PoI)
    # print("Vol path list: ", len(Vol_path_list), "PoI", len(PoI_locs))

    #Get survivors locations
    S_locs = initial_survivor_loc(PoI_locs, PoI_radii, S_count_in_PoI)

    #Get volunteer locations
    Vol_locs = initial_volunteer_loc(Vol_path_list)

    return CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, S_count_in_PoI, Vol_locs


#Get list of CC/PoI nodes visited by a certain responder
def responder_visiting_IDs(Res_paths, CC_locs, PoI_locs, num_of_nodes):
    # Get CC and PoI IDs that each responder visits
    Res_visiting_IDs_dict = {}
    count = 0
    for k in range(len(Res_paths)):
        Res_visiting_IDs = []
        for loc in Res_paths[k]:
            #CC locs and ids
            for i in range(len(CC_locs)):
                if loc == CC_locs[i]:
                    Res_visiting_IDs.append(i)
                    break
            #PoI locs and ids
            for j in range(len(PoI_locs)):
                if loc == PoI_locs[j]:
                    Res_visiting_IDs.append(len(CC_locs) + j)
                    break
        if k == 1:
            print("Res locs", num_of_nodes + k, Res_paths[k])
            print("Res ", num_of_nodes + k, Res_visiting_IDs)
        Res_visiting_IDs_dict[num_of_nodes + k] = Res_visiting_IDs
        count = count + 1
    return Res_visiting_IDs_dict


#Get list of responders who visit a certain CC/PoI node
def nodes_served_by_res_ids(Res_visiting_IDs_dict, CC_locs, PoI_locs):
    Node_visting_res_dict = {}

    for u in range(len(CC_locs) + len(PoI_locs)):
        node_list = []
        for res_id, nodes in Res_visiting_IDs_dict.items():
            # print("Res, nodes ", u, res_id, nodes)
            if u in nodes:
                # print(u, "exists in node list", node_list)
                node_list.append(res_id)

        Node_visting_res_dict[u] = node_list
    return Node_visting_res_dict


def plot_graph(G, filename):
    plt.figure()
    plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())))
    nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.draw()
    plt.savefig(filename + "_" + str(len(G.nodes())) + ".png")
    plt.close()
