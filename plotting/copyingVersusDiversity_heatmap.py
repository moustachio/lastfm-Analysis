"""
Generates plots of copy probability as a function of item entropy, pooled across all items.
"""


# ent_table format is item_id, month, ent, rel_ent, gini, unique_tags, total_annotations, topCopy, binCopy, normCopy

import sys
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
from matplotlib import pyplot as plt
import numpy as np

cursor = db.cursor()
cursorSS = dbSS.cursor()
cursorSS.execute("select * from ent_table order by item_id, month;")

firstRow = cursorSS.fetchone() # fetch just diversity from first row to fix offset
rel_ent = [firstRow[3],] 
ent = [firstRow[2],]
gini = [firstRow[4],]
topCopy = []
binCopy = []
normCopy = []

#lastVal = None
for row in cursorSS:
	iid = row[0]
	copyVal = row[7]
	#if lastVal and copyVal != None: 
	if copyVal != None and row[6] > 99:
		rel_ent.append(row[3])
		ent.append(row[2])
		gini.append(row[4])
		topCopy.append(copyVal)
		binCopy.append(row[8])
		normCopy.append(row[9])
	#lastVal = copyVal



fig = plt.figure(figsize=(24,18))
figCount = 1


for data in ('topCopy','binCopy','normCopy'):

	x = rel_ent[:-1]
	y = vars()[data]

	xmin,ymin,xmax,ymax = min(x),min(y),max(x),max(y)

	plt.subplot(3,3,figCount)
	plt.hexbin(x,y, bins='log',cmap=plt.cm.jet)
	plt.axis([xmin, xmax, ymin, ymax])
	#plt.title("Copy Probability vs. Diversity")
	plt.xlabel('rel. entropy')
	plt.ylabel(data)
	cb = plt.colorbar()
	cb.set_label('log10(N)')
	figCount += 1 

	x = ent[:-1]
	xmin,ymin,xmax,ymax = min(x),min(y),max(x),max(y)

	plt.subplot(3,3,figCount)
	plt.hexbin(x,y, bins='log',cmap=plt.cm.jet)
	plt.axis([xmin, xmax, ymin, ymax])
	#plt.title("Copy Probability vs. Diversity")
	plt.xlabel('entropy')
	plt.ylabel(data)
	cb = plt.colorbar()
	cb.set_label('log10(N)')
	figCount += 1

	x = gini[:-1]
	xmin,ymin,xmax,ymax = min(x),min(y),max(x),max(y)

	plt.subplot(3,3,figCount)
	plt.hexbin(x,y, bins='log',cmap=plt.cm.jet)
	plt.axis([xmin, xmax, ymin, ymax])
	#plt.title("Copy Probability vs. Diversity")
	plt.xlabel('gini')
	plt.ylabel(data)
	cb = plt.colorbar()
	cb.set_label('log10(N)')
	figCount += 1

fig.savefig('plots/copyingVersusDiversity_min100Anno.pdf')