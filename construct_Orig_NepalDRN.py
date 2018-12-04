from construct_NepalDRN_utility import *
import pickle
import os

#Main starts here

#---------------- Initial setup -------------------------------------------------------------------------
#Create Bhaktapur and its sub-directories
if not os.path.exists(directory):
    os.mkdir(directory)

if not os.path.exists(data_directory):
    os.mkdir(data_directory)

if not os.path.exists(plot_directory):
    os.mkdir(plot_directory)

CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, S_count_in_PoI, Vol_locs = initial_setup()
num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

print("CC:", len(CC_locs), "Start-id ", 0, "End-id", len(CC_locs) - 1)
pickle.dump(CC_locs, open(directory + "Data/" + 'CC_locs.p','wb'))

print("PoI:", len(PoI_locs), "Start-id", len(CC_locs), "End-id", len(CC_locs) + len(PoI_locs) - 1)
print("PoI locs:", [loc for loc in PoI_locs])
pickle.dump(PoI_locs, open(directory + "Data/" + 'PoI_locs.p','wb'))

print("Volunteers:", len(Vol_path_list), "Start-id", len(CC_locs) + len(PoI_locs) , "End-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list) - 1)
pickle.dump(Vol_locs, open(directory + "Data/" + 'Vol_locs.p','wb'))

print("Survivors:", len(S_locs), " Start-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list), "End-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs) - 1)
pickle.dump(S_locs, open(directory + "Data/" + 'S_locs.p','wb'))

print("Responders:", len(Res_path_list), "Start-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs), "End-id", len(CC_locs) + len(PoI_locs) + len(Vol_path_list) + len(S_locs) + len(Res_path_list) - 1)
pickle.dump(Res_path_list, open(directory + "Data/" + 'Res_paths.p','wb'))

#Write responder paths to a file
write_paths_to_a_file (Res_path_list, "w")

CC_locs = pickle.load(open(directory + "Data/CC_locs.p", "rb"))
PoI_locs = pickle.load(open(directory + "Data/PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(directory + "Data/Vol_locs.p", "rb"))
S_locs = pickle.load(open(directory + "Data/S_locs.p", "rb"))
Res_path_list = pickle.load(open(directory + "Data/Res_paths.p", "rb"))

num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

res_visiting_all_nodes = responder_visiting_IDs(Res_path_list, CC_locs, PoI_locs, num_of_nodes)
pickle.dump(res_visiting_all_nodes, open(data_directory + 'res_visiting_all_nodes.p','wb'))
print("Res_locs", Res_path_list[1])
print("Res_visiting_IDs_dict", res_visiting_all_nodes.items()[1])

node_visited_by_all_responders = nodes_served_by_res_ids(res_visiting_all_nodes, CC_locs, PoI_locs)
pickle.dump(node_visited_by_all_responders, open(data_directory + 'node_visited_by_all_responders.p','wb'))
print("Node_visting_res_dict", node_visited_by_all_responders.items()[1])

#---------------------------------END: Initial Setup -----------------------------------------------------

print("V ", num_of_nodes)
ext_filename = loc_des_folder + 'ext_position_' + str(num_of_nodes)+ '.txt'
print("Ext file name: ", ext_filename)
f = open(ext_filename,'w')


#0 7200 0 10000 0 10000
f.write("0 " + str(total_simulation_time + 600) + " 0 " + str(X) + " 0 " + str(Y) + "\n")

start_time = 0
end_time = total_simulation_time + 60

for t in range (start_time, end_time, snapshot_time_interval):
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

