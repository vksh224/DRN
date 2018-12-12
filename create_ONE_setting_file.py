import pickle
import os
from constants import *

data_directory = directory + "Data/"

CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)
print("CC PoI Vol S", len(CC_locs), len(PoI_locs), len(Vol_locs), len(S_locs))

setting_files = os.listdir(setting_directory)

for file in setting_files:
    updated_setting_lines = []
    print(file)
    index = 0
    f = open(setting_directory + file, "r")
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
    #Copy setting file in to the new list
    index = 0 #for old file

    while len(lines) > index:
        if index < dms_index:
            if "ExternalMovement.file" in lines[index]:
                updated_setting_lines.append("ExternalMovement.file = NodePosition/ext_position_" + str(V) + '.txt\n')
            elif "Group.neighborListFile" in lines[index]:
                if "bioDRN" in file:
                    updated_setting_lines.append(
                        "Group.neighborListFile = NeighborList/B_N" + str(V + len(Res_paths)) + '.txt\n')
                elif "origDRN" in file:
                    updated_setting_lines.append("Group.neighborListFile = NeighborList/O_N" + str(V + len(Res_paths)) + '.txt\n')
            else:
                updated_setting_lines.append(lines[index])
            index += 1

        elif index < first_cd_index:
            print("Here: ", index, first_cd_index)
            index = first_cd_index + 1

            updated_setting_lines.append("Group.DMS=" + str(len(Res_paths)) + "\n")
            path_count = 1
            #Write new waypoints
            for res_path in Res_paths:
                line_str = "Group.waypoints" + str(path_count) + " = "
                for coor in res_path:
                    line_str += str(coor[0]) + ", " + str(coor[1]) + ", "
                path_count += 1
                updated_setting_lines.append(line_str + "\n")

            print("First CD", len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs))
            updated_setting_lines.append("\nGroup.firstCD= " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)) + "\n")

        else:
            #CCs
            if "Group1.nrofHosts" in lines[index]:
                updated_setting_lines.append("Group1.nrofHosts= " + str(len(CC_locs)) + '\n')

            elif "Group2.nrofHosts" in lines[index]:
                updated_setting_lines.append("Group2.nrofHosts= " + str(len(PoI_locs)) + "\n")

            elif "Group3.nrofHosts" in lines[index]:
                updated_setting_lines.append("Group3.nrofHosts= " + str(len(Vol_locs)) + "\n")

            elif "Group4.nrofHosts" in lines[index]:
                updated_setting_lines.append("Group4.nrofHosts= " + str(len(S_locs)) + "\n")

            elif "Group5.nrofHosts" in lines[index]:
                updated_setting_lines.append("Group5.nrofHosts= " + str(len(Res_paths)) + "\n")

            elif "Events1.hosts" in lines[index]:
                updated_setting_lines.append("Events1.hosts= " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs)) + ", " + str(len(S_locs)) + "\n")

            elif "Events1.tohosts" in lines[index]:
                updated_setting_lines.append("Events1.tohosts= 0, " + str(len(CC_locs)) + "\n")

            else:
                updated_setting_lines.append(lines[index])

            index += 1

    f = open(setting_directory + file, "w")
    for ind in range(len(updated_setting_lines)):
        f.write(updated_setting_lines[ind])

    f.close()








