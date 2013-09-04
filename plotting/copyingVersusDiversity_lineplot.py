import sys
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
from matplotlib import pyplot as plt
import numpy as np

cursor = db.cursor()
cursorSS = dbSS.cursor()
cursorSS.execute("select * from ent_table order by item_id, month;")

data = {round(i,2):[] for i in np.arange(0,1.01,0.01)}

firstRow = cursorSS.fetchone() # fetch just diversity from first row to fix offset
rel_ent = [firstRow[3],] 
#ent = [firstRow[2],]
gini = [firstRow[4],]
topCopy = []
#binCopy = []
#normCopy = []

for row in cursorSS:
	copyVal = row[7]
	if copyVal != None:
		data[round(row[3],2)].append(copyVal)
