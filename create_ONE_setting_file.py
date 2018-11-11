import pickle
import os
from constants import *

CC_locs = pickle.load(open(directory + "Data/CC_locs.p", "rb"))
PoI_locs = pickle.load(open(directory + "Data/PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(directory + "Data/Vol_locs.p", "rb"))
S_locs = pickle.load(open(directory + "Data/S_locs.p", "rb"))
Res_paths = pickle.load(open(directory + "Data/Res_paths.p", "rb"))

setting_directory = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/Nepal/"

setting_files = os.listdir(setting_directory)

updated_setting_lines = []

for file in setting_files[:1]:
    print(file)
    index = 0
    f = open(setting_directory + file, "r")
    lines = f.readlines()
    dms_index = 0
    first_cd_index = 0
    for line in lines:
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
        updated_setting_lines.append(lines[index])
        index += 1

    elif index < first_cd_index:
        print("Here: ", index, first_cd_index)
        index = first_cd_index + 1

        updated_setting_lines.append("Group.DMS =" + str(len(Res_paths)) + "\n")
        path_count = 1
        #Write new waypoints
        for res_path in Res_paths:
            line_str = "Group.waypoints" + str(path_count) + " = "
            for coor in res_path:
                line_str += str(coor[0]) + ", " + str(coor[1]) + ", "
            path_count += 1
            updated_setting_lines.append(line_str + "\n")

        updated_setting_lines.append("\nGroup.firstCD = " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)) + "\n")

    else:
        #CCs
        if "Group1.nrofHosts" in lines[index]:
            updated_setting_lines.append("Group1.nrofHosts = " + str(len(CC_locs)) + '\n')

        elif "Group2.nrofHosts" in lines[index]:
            updated_setting_lines.append("Group2.nrofHosts = " + str(len(PoI_locs)) + "\n")

        elif "Group1=3.nrofHosts" in lines[index]:
            updated_setting_lines.append("Group3.nrofHosts = " + str(len(Vol_locs)) + "\n")

        elif "Group4.nrofHosts" in lines[index]:
            updated_setting_lines.append("Group4.nrofHosts = " + str(len(S_locs)) + "\n")

        elif "Group5.nrofHosts" in lines[index]:
            updated_setting_lines.append("Group5.nrofHosts = " + str(len(Res_paths)) + "\n")

        elif "Events1.hosts" in lines[index]:
            updated_setting_lines.append("Events1.hosts = " + str(len(CC_locs) + len(PoI_locs) + len(Vol_locs)) + ", " + str(len(S_locs)) + "\n")

        elif "Events1.tohosts" in lines[index]:
            updated_setting_lines.append("Events1.tohosts = 0, " + str(len(CC_locs)) + "\n")

        else:
            updated_setting_lines.append(lines[index])

        index += 1

f = open(setting_directory + file, "w")
for ind in range(len(updated_setting_lines)):
    f.write(updated_setting_lines[ind])

f.close()








