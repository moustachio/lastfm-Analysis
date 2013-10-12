import sys
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import tsem # standard error function

cursor = db.cursor()
cursorSS = dbSS.cursor()
cursorSS.execute("select * from ent_table order by item_id, month;")

data = {round(i,2):[] for i in np.arange(0,1.01,0.01)}

###### NEED TO FIX THIS SO VALUES LINE UP PROPERLY!!!

firstRow = cursorSS.fetchone() # fetch just diversity from first row to fix offset
rel_ent = [firstRow[3],] 
#ent = [firstRow[2],]
gini = [firstRow[4],]
topCopy = []
#binCopy = []
#normCopy = []

lastEnt = firstRow[3]
for row in cursorSS:
	copyVal = row[7]
	if copyVal != None:
		data[round(lastEnt,2)].append(copyVal)
	lastEnt = row[3]

x = sorted(data.keys())
y = [np.mean(data[i]) if data[i] else 0 for i in sorted(data)]
err = [2*tsem(data[i]) if data[i] else 0 for i in sorted(data)]
fig = plt.figure()
plt.errorbar(x,y,err)
fig.savefig('CvD_lineplot.pdf')