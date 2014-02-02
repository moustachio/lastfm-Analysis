"""
Script for calculating entropy measures across all time for all items in the annotation dataset.

Calculates entropy measure for tag distributuions of all unique items for each month in which those items received annotations.
"""

import sys 
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
from distAnalysis import *
import collections
import numpy as np
import time

cursor=db.cursor()
cursor.execute("DROP TABLE IF EXISTS ent_users;") # This should just drop the entropy table
print 'table dropped'

cursor.execute("CREATE TABLE ent_users (user_id int unsigned, month date, \
	ent_cumulative FLOAT, rel_ent_cumulative FLOAT, gini_cumulative FLOAT, tags_cumulative int, anno_cumulative int, \
	ent_current FLOAT, rel_ent_current FLOAT, gini_current FLOAT, tags_current int, anno_current int, \
	topCopy FLOAT, binCopy FLOAT, normCopy FLOAT, seq tinyint unsigned, \
    index(user_id), index(month)) ENGINE=innodb DEFAULT CHARSET=latin1;") 
closeDBConnection(cursor) 
print 'new table generated'

cursor=db.cursor()
cursorSS=dbSS.cursor()
cursorSS.execute("select * from lastfm_annotations order by user_id, tag_month;")
print 'query executed'
	

dictCumulative = {}
dictCurrent = {}
#new date and id
date1 = 0
id1 = 0
#old date and id
date2 = 0
id2 = 0
count = 0
seq = 0
start = time.time()
for row in cursorSS:
	# this is just an efficiency thing. 
	if count>0 and count % 100000 == 0:
		db.commit()
		print count, (time.time()-start) / 60.0
	date1 = row[4]
	id1 = row[0] # same as old, this is USER ID
	#used when new item
	if not dictCumulative:
		dictCumulative = {row[0] : []} 
		dictCurrent = {row[0] : []} 
	#used when new month. calc ent rel_ent and gini and put them in db
	if ((date1 != date2) or (id1 != id2)) and count > 0: 
		
		en_cumulative = ent(dictCumulative[id2])
		e_cumulative = en_cumulative[0]
		re_cumulative = en_cumulative[1]
		n_cumulative = en_cumulative[2]
		sm_cumulative = en_cumulative[3]

		en_current = ent(dictCurrent[id2])
		e_current = en_current[0]
		re_current = en_current[1]
		n_current = en_current[2]
		sm_current = en_current[3]

		gin_cumulative = gini(dictCumulative[id2])
		gin_current = gini(dictCurrent[id2])	

		cursor.execute("insert ignore into ent_users (user_id, month, \
			ent_cumulative, rel_ent_cumulative, gini_cumulative, tags_cumulative, anno_cumulative, \
			ent_current, rel_ent_current, gini_current, tags_current, anno_current, \
			seq) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id2,date2,e_cumulative,re_cumulative,gin_cumulative,n_cumulative,sm_cumulative,e_current,re_current,gin_current,n_current,sm_current,seq)) 
		
		if date1 != date2:
			dictCurrent = {row[0]: []}
		if id1 != id2:
			dictCumulative = {row[0] : []}
			dictCurrent = {row[0]: []}
			seq=0
		else:
			seq += 1
	#add new value to key
	dictCumulative[row[0]].append(row[3])
	dictCurrent[row[0]].append(row[3])
	count += 1
	date2 = row[4]
	id2 = row[0]



# Final insert
en_cumulative = ent(dictCumulative[id2])
e_cumulative = en_cumulative[0]
re_cumulative = en_cumulative[1]
n_cumulative = en_cumulative[2]
sm_cumulative = en_cumulative[3]

en_current = ent(dictCurrent[id2])
e_current = en_current[0]
re_current = en_current[1]
n_current = en_current[2]
sm_current = en_current[3]

gin_cumulative = gini(dictCumulative[id2])
gin_current = gini(dictCurrent[id2])	

cursor.execute("insert ignore into ent_users (user_id, month, \
	ent_cumulative, rel_ent_cumulative, gini_cumulative, tags_cumulative, anno_cumulative, \
	ent_current, rel_ent_current, gini_current, tags_current, anno_current, \
	seq) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id2,date2,e_cumulative,re_cumulative,gin_cumulative,n_cumulative,sm_cumulative,e_current,re_current,gin_current,n_current,sm_current,seq)) 

closeDBConnection(cursor)	 
closeDBConnection(cursorSS)