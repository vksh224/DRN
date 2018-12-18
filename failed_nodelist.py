import networkx as nx
import pickle
import os
import numpy as np
from constants import *

print("======== Failed node list: " + directory)

s = '0 ' + str(total_simulation_time) + "\n"
r = []

if not os.path.exists(failed_node_folder):
    os.makedirs(failed_node_folder)

data_directory = directory + "Data/"

CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

N = [i for i in range(len(CC_locs), V)]
n = len(N)

for t in range(0, total_simulation_time, network_construction_interval):

    r.extend(np.random.choice(N,size = int(p * n),replace = False))
    s = s + str(t) + ' ' + " ".join(str(x) for x in r) + '\n'
    N = [u for u in N if u not in r]

f = open(failed_node_folder + 'failed_nodelist_' + str(V + len(Res_paths)) + '.txt','w')
f.write(s)
f.close()
print(s)



