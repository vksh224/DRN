import networkx as nx

def relabel(G,h,s):

    orig = G.nodes()
    orig = sorted(orig)
    tran = [(i + len(G)) for i in orig]
    mh = []
    print ('TRAN', tran)
    print ('ORIG',orig)

    mf = {}
    mb = {}
    m = {}
    for i in range(len(orig)):
        mf[orig[i]] = tran[i]
        mb[tran[i]] = orig[i]

    G = nx.relabel_nodes(G, mf)
    for u in tran:
        if mb[u] in h:
            mh.append(orig[0])
            m[u] = orig[0]
            orig = orig[1:]


    for u in tran:
        if mb[u] not in h:
            m[u] = orig[0]
            orig = orig[1:]

    G = nx.relabel_nodes(G,m)
    if s == 'od':
        return G,mh
    else:
        return G,mh


def neighbor(gD,mgD,m,hD,cnt):

    fname = 'od'
    gD = gD.reverse()
    if mgD != None:
        mgD = mgD.reverse()

    gD,hD = relabel(gD,hD,fname)
    nx.write_gml(gD,fname + '.gml')
    if mgD != None:
        mgD,hD = relabel(mgD,hD,'md')
        nx.write_gml(mgD, 'md.gml')

    sOD_C = ''
    sOD_S = str([each for each in hD]) + '\n'

    for u in gD.nodes():
        sOD_C += str(cnt * 600) + ' ' + str(u)
        for v in gD.successors(u):
            sOD_C += ' ' + str(v)

        sOD_C += '\n'

    fnameOD_C = "positionOD_C" + str(len(gD)) + ".txt"
    fnameOD_S = "sinksOD_S" + str(len(gD)) + ".txt"

    if mgD != None:
        fnameMD_S = "sinksMD_S" + str(len(mgD)) + ".txt"

    with open(fnameOD_C, "a") as myfile:
        myfile.write(sOD_C)

    with open(fnameOD_S, "a") as myfile:
            myfile.write(sOD_S)

    if mgD != None:
        with open(fnameMD_S, "a") as myfile:
                myfile.write(sOD_S)

    if mgD != None:
        print ("Watch mapped:", [mgD.in_degree(u) for u in hD])
    print ("Watch original:", [gD.in_degree(u) for u in hD])

    if mgD == None:
        return

    fnameMD_C = "positionMD_C" + str(len(mgD)) + ".txt"

    sMD_C = ''
    for u in mgD.nodes():
        sMD_C += str(cnt * 600) + ' ' + str(u)
        for v in mgD.successors(u):
            sMD_C += ' ' + str(v)

        sMD_C += '\n'

    with open(fnameMD_C, "a") as myfile:
        myfile.write(sMD_C)

def writers(gD,coor,cnt):


    sMD_C = ''

    for u in gD.nodes():
        sMD_C += str(cnt * 600) + ' ' + str(u) + ' ' + str(coor[u][0]) + ' ' + str(coor[u][1]) + '\n'

    fnameMD_C = "position_COOR" + str(len(gD)) + ".txt"


    with open(fnameMD_C, "a") as myfile:
            myfile.write(sMD_C)

