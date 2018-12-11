import networkx as nx
import os
import numpy as np

curr = os.getcwd()
os.chdir(curr)

#Number of timeslots
timeslots = 13

#Percentage of nodes failed
p = 0.02

s = ''
r = []

#Input Original DRN
os.chdir('/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur/')

G = nx.read_gml('Orig_NepalDRN_900.gml')

N = G.nodes()
n = len(N)
print ('Number of nodes:',n)

for i in range(timeslots):

    r.extend(np.random.choice(N,size = int(p * n),replace = False))
    s = s + str(i * 900) + ' ' + " ".join(str(x) for x in r) + '\n'
    N = [u for u in N if u not in r]

print (s)

f = open('failed_nodelist.txt','w')
f.write(s)
f.close()


