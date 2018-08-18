from genTop import *


folder = "kathmandu/"
G = nx.read_gml(folder + 'inputDRN.gml')
GBD = nx.read_gml(folder + 'GBD.gml')
RA = randomDRN(G, GBD)
S = spanning(RA.copy())

KR2 = kregular(RA,2)
KR4 = kregular(RA,4)
KR8 = kregular(RA,8)
