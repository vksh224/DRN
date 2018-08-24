#Ideal Ratio hub:0.02
#Sub Ratio:

#Number of nodes in DRN graph
ND = 100

#Minimum of paths from existing reference GRN and newly considered node
kh = 15
kn = 2

#Probability of edge existence in Erdos Renyi Graph
p = 0.5

#Distribution ratio of hub, sub and non.
hR = 0.05
sR = 0.3

#Deployment Area
Xlim = 100
Ylim = 100

#Transmission Range
TRan = 50

#Number of reassigned nodes
r = 0.05 * ND

sink = 0.05 * ND

#Iterations
iter = 10

gsink = 'gsink.txt'
dsink = 'dsink.txt'

#Test Inputs:

#<ND,Xlim,YLim,TRan>
#<50,100,100,50>
#<100,300,300,50>
#<60,20,20,50>
#<80,25,25,50>
#<100,30,30,50>