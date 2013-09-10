"""
Calculates the self-information of each tag for each month, recording it in a new tag_info table.
self-information is defined as -log(P(tag)). See https://en.wikipedia.org/wiki/Self-information
"""

import sys
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
from numpy import log2

f = open('../Results/tagFreqByMonth.tsv')
cursor = db.cursor()
cursor.execute("drop table if exists tag_info;")
cursor.execute("CREATE TABLE `tag_info` (\
	`date` DATE NULL,\
	`tag_id` MEDIUMINT(8) UNSIGNED NULL,\
	`info` FLOAT UNSIGNED NULL,\
	INDEX `date` (`date`),\
	INDEX `tag_id` (`tag_id`));")
closeDBConnection(cursor)

lastDate = None

dist = {}

for line in f:
	line = line.strip().split('\t')
	date = line[0]
	tag = int(line[1])
	freq = int(line[2])
	if lastDate and (date != lastDate):
		print lastDate
		total = float(sum(dist.values()))
		cursor = db.cursor()
		for t in dist:
			info = -log2(dist[t]/total)
			cursor.execute("insert into tag_info (date,tag_id,info) values (%s,%s,%s);", (lastDate,t,info))
		closeDBConnection(cursor)

	dist[tag] = dist.get(tag,0)+freq
	lastDate = date