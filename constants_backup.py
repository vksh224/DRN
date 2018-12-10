GRN_directory ="Yeast_Data_New/"
directory = "Bhaktapur/"
data_directory = "Bhaktapur/Data/"
plot_directory = "Bhaktapur/Plots/"

#loc_des_folder = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/NodePosition/"
#setting_directory = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/Nepal/"

# loc_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NodePosition/"
# neigh_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NeighborList/"
#setting_directory = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/Nepal/"

loc_des_folder = "/Users/vijay/BioDRN_ONE/BioDRN/src/NodePosition/"
neigh_des_folder = "/Users/vijay/BioDRN_ONE/BioDRN/src/NeighborList/"
setting_directory = "/Users/vijay/BioDRN_ONE/BioDRN/src/Nepal/"

input_grn = "Yeast_Ordered.gml"

X = 10000
Y = 10000

lX = 1000
hX = 5000
lY = 3000
hY = 6000

snapshot_time_interval = 300
#in minutes (equivalent to 12 hours)
total_simulation_time = 3600

#15 minutes
network_construction_interval = 900

no_of_CC = 1
no_of_PoI = 5
no_of_R = 30

min_no_PoIs_for_R = 2
max_no_PoI_for_R = 5

no_of_Towers = 5

min_V_in_PoI = 1
max_V_in_PoI = 3

min_S_in_PoI = 20
max_S_in_PoI = 30

min_PoI_radius= 100
max_PoI_radius = 300

bt_range = 150
vol_range = 150
tower_range = 150

#----- related to volunteer path

min_num_sides = 3
max_num_sides = 10

min_side_length = 10
max_side_length = 50
#Max side length will be given by PoI_radius

min_side_angle = 45
max_side_angle = 360

#------------------

moving_S_prob = 0.5
min_S_speed = 0.12
max_S_speed = 0.15

#In m/s
min_V_speed = 1
max_V_speed = 5