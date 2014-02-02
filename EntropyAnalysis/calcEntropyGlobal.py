"""
Script for calculating entropy measures across all time for all items in the annotation dataset.

Calculates entropy measure for tag distributuions of all unique items for each month in which those items received annotations.
"""

import sys 
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from distAnalysis import * # for gini and entropy functions
import numpy as np
import time


currentMonthDist = {}
cumulativeDist = {}

f = open('../Results/annotations_date-iid-tid.tsv','r')
out = open('../Results/ent_global','w')
out.write('date\tentropy\trelativeEntropy\tgini\ttags\tannotations\tannoPerTag\tentropy.cumulative\trelativeEntropy.cumulative\tgini.cumulative\ttags.cumulative\tannotations.cumulative\tannoPerTag.cumulative\n')

lastDate = None
for line in f:
	line = line.strip().split('\t')
	date = line[4]
	if lastDate and (date != lastDate):
		giniCum = gini(cumulativeDist)
		entValsCum = ent(cumulativeDist)
		giniCurrent = gini(currentMonthDist)
		entValsCurrent = ent(currentMonthDist)
		result = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (lastDate,entValsCurrent[0],entValsCurrent[1],giniCurrent,entValsCurrent[2],entValsCurrent[3],entValsCurrent[3]/float(entValsCurrent[2]),entValsCum[0],entValsCum[1],giniCum,entValsCum[2],entValsCum[3],entValsCum[3]/float(entValsCum[2]))
		out.write(result)
		print result
		currentMonthDist = {}
	tag = line[3]
	currentMonthDist[tag] = currentMonthDist.get(tag,0)+1
	cumulativeDist[tag] = cumulativeDist.get(tag,0)+1
	lastDate = date

giniCum = gini(cumulativeDist)
entValsCum = ent(cumulativeDist)
giniCurrent = gini(currentMonthDist)
entValsCurrent = ent(currentMonthDist)
result = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (lastDate,entValsCurrent[0],entValsCurrent[1],giniCurrent,entValsCurrent[2],entValsCurrent[3],entValsCurrent[3]/float(entValsCurrent[2]),entValsCum[0],entValsCum[1],giniCum,entValsCum[2],entValsCum[3],entValsCum[3]/float(entValsCum[2]))
out.write(result)
out.close()