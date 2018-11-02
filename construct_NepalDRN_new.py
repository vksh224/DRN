from construct_NepalDRN_utility import *

#Main starts here

#---------------- Initial setup -------------------------------------------------------------------------

CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, Vol_locs = initial_setup()

old_track_node_id = 0
new_track_node_id = len(CC_locs)
print("CC:", len(CC_locs), "Start-id ", old_track_node_id, "End-id", new_track_node_id - 1)

old_track_node_id = new_track_node_id
new_track_node_id += len(PoI_locs)
print("PoI:", len(PoI_locs), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)

old_track_node_id = new_track_node_id
new_track_node_id += len(Res_path_list)
print("Responders:", len(Res_path_list), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)

old_track_node_id = new_track_node_id
new_track_node_id += len(Vol_path_list)
print("Volunteers:", len(Vol_path_list), "Start-id", old_track_node_id, "End-id", new_track_node_id - 1)
print ("Volunteer locs: ", [loc for loc in Vol_locs])

old_track_node_id = new_track_node_id
new_track_node_id += len(S_locs)
print("Survivors:", len(S_locs), " Start-id", old_track_node_id, "End-id", new_track_node_id)

#Write responder paths to a file
write_paths_to_a_file (Res_path_list + Vol_path_list, "w")

#---------------------------------END: Initial Setup -----------------------------------------------------

loc_des_folder = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/NodePosition/"
t = 0

f = open(loc_des_folder + 'ext_position.txt','w')

#0 7200 0 10000 0 10000
f.write("0 " + str(7200) + " 0 " + str(X) + " 0 " + str(Y) + "\n")

start_time = 0
end_time = total_simulation_time

for t in range (start_time, end_time, time_interval):
    #Get starting CC_id
    node_id = 0
    #Write CC location at time t to the external movement file
    for loc in CC_locs:
        f.write(str(t * 600) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get starting PoI id
    node_id = len(CC_locs)
    #Write PoI location at time t to the external movement file
    for loc in PoI_locs:
        f.write(str(t * 600) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get Starting Volunteer id
    node_id = len(CC_locs) + len(PoI_locs) + len(Res_path_list)
    for loc in Vol_locs:
        f.write(str(t * 600) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    #Get starting survivor id
    node_id = len(CC_locs) + len(PoI_locs) + len(Res_path_list) + len(Vol_path_list)

    for loc in S_locs:
        f.write(str(t * 600) + " " + str(node_id) + " " + str(loc[0]) + " " + str(loc[1]) + "\n")
        node_id += 1

    update_survivor_loc(S_locs, t, t + time_interval)
    #update_volunteer_loc(Vol_locs, Vol_path_list, t, t + time_interval)

f.close()

