"""
Script to calculate probability of an existing tag being copied from month to month.
E.g. probability that any given tag used at t+1 is copied from the tag distribution at time t.
Calculation is performed on an user by user basis.
"""

import sys
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
import time


N = 5 # "N" for use in "topN" heuristic (typically 5)

cursor=db.cursor()
cursor.execute("update ent_users set topCopy=NULL, binCopy=NULL, normCopy=NULL where topCopy is not NULL;")
db.commit()


cursorSS=dbSS.cursor()
cursorSS.execute("select * from lastfm_annotations order by user_id, tag_month;")

lastUser = None
lastDate = None
first = True
rowCount = 0
totalTagDist = {}
currentTagDist= {}
start = time.time()

for row in cursorSS:

	if rowCount>0 and rowCount % 100000 == 0:
		db.commit()
		print rowCount, (time.time()-start) / 60.0

	user = row[0]
	tag = row[3]
	date = row[4]
	if (user != lastUser) or (date != lastDate):
		
		if not first and totalTagDist:	
			# get frequencies of top N tags
			topN = sorted(totalTagDist,key=totalTagDist.get)[-N:]
			# this gives us the frequency of the most popular tag
			n = totalTagDist[topN[-1]]

			# MEASURE 1: Binary copy or not
			binCopy=0
			# MEASURE 2: Copy from top 5 or not
			topCopy=0
			# MEASURE 3: Copy proportional to frequency in distribution
			normCopy = 0

			# calculates counts for all measures
			for t in currentTagDist:
				tCount = totalTagDist.get(t,None)
				if t in topN:
					count = currentTagDist[t]
					topCopy += count
					binCopy += count
					normCopy += count * (tCount / float(n))
				elif tCount:
					count = currentTagDist[t]
					binCopy += count
					normCopy += count * (tCount / float(n))

			total = sum(currentTagDist.values())

			cursor.execute("update ent_users set topCopy=%s, binCopy=%s, normCopy=%s where user_id=%s and month=%s", (float(topCopy) / total, float(binCopy) / total, float(normCopy) / total, lastUser, lastDate))

		if user == lastUser:
			for t in currentTagDist:
				totalTagDist[t] = totalTagDist.get(t,0)+1
		else:
			totalTagDist = {} 

		currentTagDist = {}

		if user != lastUser:
			first = True
		else:
			first = False

	currentTagDist[tag] = currentTagDist.get(tag,0)+1
	lastUser = user
	lastDate = date
	rowCount += 1

### Need to add this block (probably a cleaner way to handle it) to handle the last row...
if not first and totalTagDist:	
	# get frequencies of top N tags
	topN = sorted(totalTagDist,key=totalTagDist.get)[-N:]
	# this gives us the frequency of the most popular tag
	n = totalTagDist[topN[-1]]

	# MEASURE 1: Binary copy or not
	binCopy=0
	# MEASURE 2: Copy from top 5 or not
	topCopy=0
	# MEASURE 3: Copy proportional to frequency in distribution
	normCopy = 0

	# calculates counts for all measures
	for t in currentTagDist:
		tCount = totalTagDist.get(t,None)
		if t in topN:
			count = currentTagDist[t]
			topCopy += count
			binCopy += count
			normCopy += count * (tCount / float(n))
		elif tCount:
			count = currentTagDist[t]
			binCopy += count
			normCopy += count * (tCount / float(n))

	total = sum(currentTagDist.values())

	cursor.execute("update ent_users set topCopy=%s, binCopy=%s, normCopy=%s where user_id=%s and month=%s", (float(topCopy) / total, float(binCopy) / total, float(normCopy) / total, lastUser, lastDate))


closeDBConnection(cursor)
closeDBConnectionSS(cursorSS)
