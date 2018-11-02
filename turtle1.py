import turtle
import random


def volunteer_path(poi_loc):
    polygon = turtle.Turtle()

    num_sides = random.randint(4, 10)
    side_length = random.randint(10, poi_radius)
    angle = 360.0 / num_sides

    #polygon.speed(random.randint(1, 5))
    polygon.setposition(poi_loc)

    vol_coor_list = []
    print("Number of sides: ", num_sides)
    for i in range(num_sides):
        #print(i, polygon.position())
        vol_coor_list.append(str(polygon.position()))
        polygon.forward(side_length)
        polygon.right(angle)
    #turtle.done()
    return vol_coor_list

def allocate_volunteers():

    f_vol = open(directory + 'volunteer_paths.txt', 'w')
    vol_count = len(responders) + 1
    for poi_id in range(len(PoIs_loc)):
        for vol_id in range(PoI_Vol_count[poi_id]):
            f_vol.write("Group.waypoints" + str(vol_count) + " = ")

            vol_coor_list = volunteer_path(PoIs_loc[poi_id])
            with open(directory + "poi_" + str(poi_id) + "vol_" + str(vol_id) + '.txt', 'w') as f:
                for coor in vol_coor_list:
                    coor = coor.strip("()").split(",")
                    print ("coor: ", poi_id, vol_id, str(coor))
                    f.write(str(coor[0]) + " " + str(coor[1]) + "\n")
                    f_vol.write(str(coor[0]) + ", " + str(coor[1]) + ", ")

            vol_count += 1
            f_vol.write("\n")
            f.close()
    f_vol.close()


def allocate_responders():
    CC_PoI_locs = []

    #CC and PoI locations
    for loc in CC_loc:
        CC_PoI_locs.append(loc)
    for loc in PoIs_loc:
        CC_PoI_locs.append(loc)

    f = open(directory + 'responder_paths.txt', 'w')

    path_count = 1
    for res_path in responders:
        #print("Res : ", res_path, " ")
        line_str = "Group.waypoints" + str(path_count) +" = "

        for node_id in res_path:
            #print("Here", CC_PoI_locs[node_id], CC_PoI_locs[node_id][0], str(CC_PoI_locs[node_id][1]), "there")
            line_str += str(CC_PoI_locs[node_id][0]) + ", " + str(CC_PoI_locs[node_id][1]) + " , "
        f.write(line_str + "\n")
        path_count += 1
    f.close()

#Main starts here
poi_radius = 200

CC_loc = [(2809, 4516)]
PoIs_loc = [(2190, 5390), (2370, 4530), (2940, 5240), (3690, 4160), (4230, 4700), (4620, 4990)]
PoI_Vol_count = [2, 2, 3, 3, 3, 2]
responders = [[0, 2, 4, 0], [0, 3, 2, 0], [0, 3, 1, 3, 0], [0, 4, 0], [0, 5, 6, 0], [0, 6, 0], [0, 6, 5, 4, 0], [0, 5, 0]]

directory = "VolunteerPaths/"

#Generate responder paths
# allocate_responders()

#Generate volunteer paths
allocate_volunteers()