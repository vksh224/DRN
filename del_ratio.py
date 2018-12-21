#!/usr/bin/python

'''
A simple to compute the delivery ratio of the messages (with 95% CI) under
various scenarios.
'''

import csv
# import gen_stats as gs
import math
import os
import pickle


# Average of a list of numbers
def get_average(numbers=[]):
    avg = 0.0
    n = len(numbers)
    for i in range(0, n):
        avg += numbers[i]
    if n > 0:
        avg /= n
    return avg


# Std. Dev. of a list of numbers
def get_std_dev(num=[]):
    n = len(num)
    avg = get_average(num)

    variance = 0.0
    for i in range(0, n):
        variance += (num[i] - avg) ** 2
    if n > 0:
        variance /= n
    std = variance ** 0.5
    return std


# Get a named statistic from the MessageStats report file
def get_stat(file_name, stat_name):
    result = 0.0
    with open(file_name, 'r') as report:
        reader = csv.reader(report, delimiter=' ')
        for line in reader:
            if line[0].find(stat_name) == 0:
                result = float(line[1])
                break

    return result


def get_energy_stat(file_name, time):
    # print("filename", file_name)
    available_energy = 0
    alive_nodes = -1
    with open(file_name, 'r') as report:
        reader = csv.reader(report, delimiter=' ')
        for line in reader:
            if abs(float(line[0]) - float(time)) < 1 and line[1].find('available_energy') == 0:
                available_energy = float(line[2])
                alive_nodes = float(line[3])
                break

    # print("time", time, "energy", available_energy, "nodes", alive_nodes)
    return available_energy, alive_nodes


# Main starts here
ONE_directory = "/mounts/u-spa-d2/grad/vksh224/BioDRN_ONE/BioDRN/src/"

routers = ('BioDRNRouter',)
endTimes = ('3600', '10800', '18000')
topologies = ('O', 'B', 'R', 'S', 'K2', 'K4')


# Scenario.name = %%Group.router%%_%%Scenario.endTime%%_%%Group.neighborListFile%%

ONE_Experiments = "ONE_Experiments"

if not os.path.exists(ONE_Experiments):
    os.mkdir(ONE_Experiments)

for option in range(1,2):
    for router in routers:
        print("\nRouter " + router)
        for top in topologies:
            print("Top", top)
            for time in endTimes:
                del_ratio = []
                latency = []
                hop_count = []
                overhead = []
                available_energy_list = []
                alive_nodes_list = []
                for run in range(1,2):
                    data_directory = "Bhaktapur_" + str(option) + "/" + str(run) + "/Data/"

                    CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
                    PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
                    Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
                    S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
                    Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

                    # This is not consistent with V from other files. Here, it includes the responders too
                    V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs) + len(Res_paths)
                            #reports/BioDRNRouter_3600_NeighList/1_0/B_214.txt_MessageStatsReport.txt
                    fname = ONE_directory + "reports/%s_%s_NeighborList/%s_%s/%s_%s.txt_MessageStatsReport.txt" % (router, time, option, run, top, V)
                    if os.path.isfile(fname):
                        del_ratio.append(get_stat(fname, 'delivery_prob'))
                        latency.append(get_stat(fname, "latency_avg"))
                        hop_count.append(get_stat(fname, "hopcount_avg"))
                        overhead.append(get_stat(fname, "overhead_ratio"))

                    else:
                        print("Stat file not found", fname)

                    energyfname = ONE_directory + "reports/%s_%s_NeighborList/%s_%s/%s_%s.txt_EnergyLevelReport.txt" % (
                    router, time, option, run, top, V)

                    if os.path.isfile(fname):
                        available_energy, alive_nodes = get_energy_stat(energyfname, time)
                        available_energy_list.append(available_energy)
                        alive_nodes_list.append(alive_nodes)

                    # else:
                    #     print("Energy file not found", energyfname)

                # print("PDR", del_ratio)
                # print("Lat", latency)
                # print("Over", overhead)
                # print("Ener", available_energy_list)
                # print("nodes", alive_nodes_list)

                # Average delivery ratio
                avg_del = get_average(del_ratio)
                avg_latency = get_average(latency)
                avg_hop = get_average(hop_count)
                avg_overhead = get_average(overhead)
                avg_available_energy = get_average(available_energy_list)
                avg_alive_nodes = get_average(alive_nodes_list)

                # sd = get_std_dev(del_ratio)
                # ci = gs.confidence_interval_mean(rng_max, sd)

                print ('%s %.2f %.2f %.2f %.2f %.2f %.2f' % (
                time, avg_del, avg_latency, avg_hop, avg_overhead, avg_available_energy, avg_alive_nodes))
