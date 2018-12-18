import pickle
import os
import sys
from constants import *


option = sys.argv[1]
run = sys.argv[2]

print("======== Create ONE setting files: " + directory)
data_directory = directory + "Data/"

CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

#This is not consistent with V from other files. Here, it includes the responders too
V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs) + len(Res_paths)
print("CC PoI Vol S: ", len(CC_locs), len(PoI_locs), len(Vol_locs), len(S_locs))

#setting_files = os.listdir(setting_directory)
sample_setting_file = core_setting_directory + "bhaktapur_origDRN_200.txt"

# if not os.path.exists(setting_directory):
#     os.mkdir(setting_directory)

option_run = str(option) + "_" + str(run)
file = open(core_setting_directory + "setting_" + option_run + ".txt", "w")

index = 0
f = open(sample_setting_file, "r")
lines = f.readlines()
dms_index = -1
first_cd_index = -1
for line in lines:
    #print(line)
    line_arr = line.split("=")
    if line_arr[0] == "Group.DMS":
        dms_index = index

    if line_arr[0].strip() == "Group.firstCD":
        first_cd_index = index

    index += 1
f.close()

print("DMS Index: ", dms_index, "First CD Index: ", first_cd_index )
#Copy setting file in to the new file
index = 0 #for old file

while len(lines) > index:
    if index < dms_index:
        if "ExternalMovement.file" in lines[index]:
            file.write("ExternalMovement.file = NodePosition/ext_position_" + str(V) + '.txt\n')

        elif "Group.neighborListFile" in lines[index]:
            file.write("Group.neighborListFile = [NeighborList/" + option_run + "/O_" + str(
                V) + ".txt; NeighborList/" + option_run + "/B_" + str(
                V) + '.txt; NeighborList/' + option_run + "/S_" + str(
                V) + '.txt; NeighborList/' + option_run + "/R_" + str(
                V) + '.txt; NeighborList/' + option_run + "/K2_" + str(
                V) + '.txt; NeighborList/' + option_run + "/K4_" + str(V) + '.txt] \n')

        elif "Group.failedNodeListFile" in lines[index]:
            file.write("Group.failedNodeListFile = FailedNodeList/" + option_run + "/failed_nodelist" + str(V) + '.txt\n')

        else:
            file.write(lines[index])
        index += 1

    elif index < first_cd_index:
        if debug_mode:
            print("Here: ", index, first_cd_index)

        index = first_cd_index + 1

        file.write("Group.DMS=" + str(len(Res_paths)) + "\n")
        path_count = 1
        #Write new waypoints
        for res_path in Res_paths:
            line_str = "Group.waypoints" + str(path_count) + " = "
            for coor in res_path:
                line_str += str(coor[0]) + ", " + str(coor[1]) + ", "
            path_count += 1
            file.write(line_str + "\n")

        if debug_mode:
            print("First CD", len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs))

        file.write("\nGroup.firstCD= " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)) + "\n")

    else:
        #CCs
        if "Group1.nrofHosts" in lines[index]:
            file.write("Group1.nrofHosts= " + str(len(CC_locs)) + '\n')

        elif "Group2.nrofHosts" in lines[index]:
            file.write("Group2.nrofHosts= " + str(len(PoI_locs)) + "\n")

        elif "Group3.nrofHosts" in lines[index]:
            file.write("Group3.nrofHosts= " + str(len(Vol_locs)) + "\n")

        elif "Group4.nrofHosts" in lines[index]:
            file.write("Group4.nrofHosts= " + str(len(S_locs)) + "\n")

        elif "Group5.nrofHosts" in lines[index]:
            file.write("Group5.nrofHosts= " + str(len(Res_paths)) + "\n")

        elif "Events1.hosts" in lines[index]:
            file.write("Events1.hosts= " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs)) + ", " + str(len(S_locs)) + "\n")

        elif "Events1.tohosts" in lines[index]:
            file.write("Events1.tohosts= 0, " + str(len(CC_locs)) + "\n")

        else:
            file.write(lines[index])

        index += 1

file.close()








