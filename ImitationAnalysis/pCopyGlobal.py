"""
Script to calculate probability of an existing tag being copied from month to month.
E.g. probability that any given tag used at t+1 is copied from the tag distribution at time t.
This determines the GLOBAL level of copying across the whole folksonomy.

Note that the top-5 copying heuristic may not make sense here...would we not want instead the proportion of annotations that were copies of an existing tag for the corresponding item? 
Need to revise how this works I think. Perhaps by revisiting plots showing percentage of annotations coming from the X percent most popular tags?
"""

N = 5 # "N" for use in "topN" heuristic (typically 5)

f = open('../Results/tagFreqByMonth.tsv')
out = open('../Results/globalCopyValues','w')
out.write('date\ttopCopy\tbinCopy\tnormCopy\n')

lastDate = None

line = f.readline().strip().split('\t')
firstDate = line[0]
tag = int(line[1])
freq = int(line[2])

date = firstDate

totalTagDist = {tag:freq}
currentTagDist= {}

while date == firstDate:
	line = f.readline().strip().split('\t')
	date = line[0]
	tag = int(line[1])
	freq = int(line[2])
	if date != firstDate:
		currentTagDist = {tag:freq}
		lastDate = date
	else:
		totalTagDist[tag] = totalTagDist.get(tag,0)+freq

for line in f:
	line = line.strip().split('\t')
	date = line[0]
	tag = int(line[1])
	freq = int(line[2])
	if date != lastDate:

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
		result = lastDate+'\t%s\t%s\t%s\n' % (float(topCopy) / total, float(binCopy) / total, float(normCopy) / total)
		print result
		out.write(result)

		for t in currentTagDist:
			totalTagDist[t] = totalTagDist.get(t,0)+currentTagDist[t]

		currentTagDist = {}

	currentTagDist[tag] = currentTagDist.get(tag,0)+freq
	lastDate = date

out.close()
