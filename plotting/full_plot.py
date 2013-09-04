
import sys 
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
import matplotlib.pyplot as plt

cursorSS=dbSS.cursor()
cursorSS.execute("select * from full_table;")

ent=[]
rel_ent=[]
gini=[]
for row in cursorSS:
    ent.append(row[1])
    rel_ent.append(row[2])
    gini.append(row[3])
    


#plt.plot(ent)
plt.plot(rel_ent, label='rel. entropy')
plt.plot(gini, label='gini')
plt.ylabel('Values')
plt.xlabel('Item Age (months)')
plt.legend()
plt.show()

