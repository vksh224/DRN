from construct_NepalDRN_utility import *
import pickle

#Main starts here

#---------------- Initial setup -------------------------------------------------------------------------

CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, S_count_in_PoI, Vol_locs = initial_setup()

old_track_node_id = 0
new_track_node_id = len(CC_locs)
print("CC:", len(CC_locs), "Start-id ", old_track_node_id, "End-id", new_track_node_id - 1)
pickle.dump(CC_locs, open(directory + "Data/" + 'CC_locs.p','wb'))

old_track_node_id = new_track_node_id
new_track_node_id += len(PoI_locs)
print("PoI:", len(PoI_locs), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)
print("PoI locs:", [loc for loc in PoI_locs])
pickle.dump(PoI_locs, open(directory + "Data/" + 'PoI_locs.p','wb'))

old_track_node_id = new_track_node_id
new_track_node_id += len(Vol_path_list)
print("Volunteers:", len(Vol_path_list), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)
pickle.dump(Vol_locs, open(directory + "Data/" + 'Vol_locs.p','wb'))

old_track_node_id = new_track_node_id
new_track_node_id += len(S_locs)
print("Survivors:", len(S_locs), " Start-id", old_track_node_id, "End-id", new_track_node_id)
pickle.dump(S_locs, open(directory + "Data/" + 'S_locs.p','wb'))


old_track_node_id = new_track_node_id
new_track_node_id += len(Res_path_list)
print("Responders:", len(Res_path_list), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)
pickle.dump(Res_path_list, open(directory + "Data/" + 'Res_paths.p','wb'))

#Write responder paths to a file
write_paths_to_a_file (Res_path_list, "w")

#---------------------------------END: Initial Setup -----------------------------------------------------

f = open(loc_des_folder + 'ext_position.txt','w')

#0 7200 0 10000 0 10000
f.write("0 " + str(7200) + " 0 " + str(X) + " 0 " + str(Y) + "\n")

start_time = 0
end_time = total_simulation_time


for t in range (start_time, total_simulation_time, time_interval):
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
    #S_locs = update_survivor_loc(PoI_locs, PoI_radii, S_locs, t, t + time_interval)
    Vol_locs = update_volunteer_loc(Vol_locs, Vol_path_list, t, t + time_interval)

f.close()

