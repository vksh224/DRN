import os
import matplotlib.pyplot as plt

path = '/Users/satyakiroy/PycharmProjects/DRN_Project/ONE_Experiments'
os.chdir(path)

filenames = ['O.txt','B.txt','K8.txt','R.txt','S.txt']
R = [[],[],[],[],[]]

for i in range(len(filenames)):

    f = open(filenames[i],'r')
    r = f.readlines()

    for l in r[1:]:
        cols = l.split()

        pdr = float(cols[1])
        alive = float(cols[-1])

        R[i].append((pdr,alive))

#print (len(R),len(R[0]),len(R[0][0]))

timeslot_duration = 1800.0
mode = 0

#Visualization
colorlist = ['r','g','b','black','magenta','purple']

for i in range(len(R)):
    plt.plot([j for j in range(len(R[0]))],[R[i][j][mode] for j in range(len(R[0]))],marker = 'o',color = colorlist[i])

#plt.xticks([j for j in range(len(R))],[j * timeslot_duration for j in range(len(L[i]))])
plt.show()