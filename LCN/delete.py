import os

n = 100
os.remove('od.gml')
os.remove('md.gml')

fos = str(n) + '_os.gml'
fst = str(n) + '_st.gml'

os.remove(fos)
os.remove(fst)

f_pos_c = 'position_COOR' + str(n) + '.txt'
f_pos_nm = 'positionMD_C' + str(n) + '.txt'
f_pos_no = 'positionOD_C' + str(n) + '.txt'

os.remove(f_pos_c)
os.remove(f_pos_nm)
os.remove(f_pos_no)

s_m = 'sinksMD_S' + str(n) + '.txt'
s_o = 'sinksOD_S' + str(n) + '.txt'

os.remove(s_m)
os.remove(s_o)