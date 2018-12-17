from construct_NepalDRN_utility import *
import pickle
import os

#Main starts here

#---------------- Initial setup -------------------------------------------------------------------------

#Create Bhaktapur and its sub-directories
if not os.path.exists(root_directory):
    os.mkdir(root_directory)

if not os.path.exists(directory):
    os.mkdir(directory)

data_directory = directory + "Data/"
plot_directory = directory + "Plot/"

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)

if not os.path.exists(loc_des_folder):
    os.makedirs(loc_des_folder)

CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, S_count_in_PoI, Vol_locs = initial_setup()
num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

pickle.dump(CC_locs, open(directory + "Data/" + 'CC_locs.p','wb'))
pickle.dump(PoI_locs, open(directory + "Data/" + 'PoI_locs.p','wb'))
pickle.dump(Vol_locs, open(directory + "Data/" + 'Vol_locs.p','wb'))
pickle.dump(S_locs, open(directory + "Data/" + 'S_locs.p','wb'))
pickle.dump(Res_path_list, open(directory + "Data/" + 'Res_paths.p','wb'))

if debug_mode:
    print("CC:", len(CC_locs), "Start-id ", 0, "End-id", len(CC_locs) - 1)
    print("PoI:", len(PoI_locs), "Start-id", len(CC_locs), "End-id", len(CC_locs) + len(PoI_locs) - 1)
    print("PoI locs:", [loc for loc in PoI_locs])
    print("Volunteers:", len(Vol_path_list), "Start-id", len(CC_locs) + len(PoI_locs), "End-id",
          len(CC_locs) + len(PoI_locs) + len(Vol_path_list) - 1)
    print("Survivors:", len(S_locs), " Start-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list), "End-id",
          len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs) - 1)
    print("Responders:", len(Res_path_list), "Start-id",
          len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs), "End-id",
          len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs) + len(Res_path_list) - 1)

#Write responder paths to a file
write_paths_to_a_file (Res_path_list, "w")

CC_locs = pickle.load(open(directory + "Data/CC_locs.p", "rb"))
PoI_locs = pickle.load(open(directory + "Data/PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(directory + "Data/Vol_locs.p", "rb"))
S_locs = pickle.load(open(directory + "Data/S_locs.p", "rb"))
Res_path_list = pickle.load(open(directory + "Data/Res_paths.p", "rb"))

num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

res_visiting_all_nodes = responder_visiting_IDs(Res_path_list, CC_locs, PoI_locs, num_of_nodes)
pickle.dump(res_visiting_all_nodes, open(directory + 'Data/res_visiting_all_nodes.p','wb'))

if debug_mode:
    print("Res_locs", num_of_nodes + 1, Res_path_list[1])
    print("Res_visiting_IDs_dict", num_of_nodes + 1, res_visiting_all_nodes.get(num_of_nodes + 1))

node_visited_by_all_responders = nodes_served_by_res_ids(res_visiting_all_nodes, CC_locs, PoI_locs)
pickle.dump(node_visited_by_all_responders, open(directory + 'Data/node_visited_by_all_responders.p','wb'))

if debug_mode:
    print("Node_visting_res_dict", node_visited_by_all_responders.items()[1])

#---------------------------------END: Initial Setup -----------------------------------------------------

if debug_mode:
    print("V ", num_of_nodes)

ext_filename = loc_des_folder + 'ext_position_' + str(num_of_nodes)+ '.txt'
print("Ext file name: ", ext_filename)

f = open(ext_filename,'w')

#0 7200 0 10000 0 10000
f.write("0 " + str(total_simulation_time) + " 0 " + str(X) + " 0 " + str(Y) + "\n")

for t in range (0, total_simulation_time, snapshot_time_interval):
    #Get starting CC_id
    node_id = 0

    #Write CC location at time t to the external movement file
    for loc in CC_locs:
        f.write(str(t) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get starting PoI id
    node_id = len(CC_locs)
    #Write PoI location at time t to the external movement file
    for loc in PoI_locs:
        f.write(str(t) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get starting volunteer id
    node_id = len(CC_locs) + len(PoI_locs)
    for loc in Vol_locs:
        f.write(str(t) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get starting survivor id
    node_id = len(CC_locs) + len(PoI_locs) + len(Vol_path_list)

    for loc in S_locs:
        f.write(str(t) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Note: Responders get the last few IDS in the ONE simulator
    S_locs = initial_survivor_loc(PoI_locs, PoI_radii, S_count_in_PoI)
    #########S_locs = update_survivor_loc(PoI_locs, PoI_radii, S_locs, t, t + snapshot_time_interval)
    Vol_locs = update_volunteer_loc(Vol_locs, Vol_path_list, t, t + snapshot_time_interval)

f.close()

