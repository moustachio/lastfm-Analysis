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
cursor.execute("DROP TABLE IF EXISTS ent_table;") # This should just drop the entropy table

cursor.execute("CREATE TABLE ent_table (item_id mediumint(8) unsigned, month date, ent FLOAT, rel_ent FLOAT, gini FLOAT, unique_tags mediumint(8), total_annotations mediumint(8), topCopy FLOAT, binCopy FLOAT, normCopy FLOAT, \
    index(item_id), index(month)) ENGINE=innodb DEFAULT CHARSET=latin1;") 
closeDBConnection(cursor) 

cursor=db.cursor()
cursorSS=dbSS.cursor()
cursorSS.execute("select * from lastfm_annotations order by item_id, tag_month;")
#cursorSS.execute("select * from anno_sample order by item_id, tag_month;")


dic = {}
#new date and id
date1 = 0
id1 = 0
#old date and id
date2 = 0
id2 = 0
count = 0
start = time.time()
for row in cursorSS:
	# this is just an efficiency thing. 
	if count>0 and count % 100000 == 0:
		db.commit()
		print count, (time.time()-start) / 60.0
	date1 = row[4]
	id1 = row[1]
	#used when new item
	if not dic:
		dic = {row[1] : []} 
	#used when new month. calc ent rel_ent and gini and put them in db
	if (date1 != date2 or id1 != id2) and count > 0: 
		#ent / rel ent tuple
		en = ent(dic[id2])
		e = en[0]
		re = en[1]
		n = en[2]
		sm = en[3]
		gin = gini(dic[id2])
		cursor.execute("insert ignore into ent_table (item_id, month, ent, rel_ent, gini, unique_tags, total_annotations) values (%s,%s,%s,%s,%s,%s,%s)",(id2,date2,e,re,gin,n,sm)) # names need to match what you defined in the table above
		#used when new id. creates new dic. Only need to do this check if the other one passes, so no need to check for count>0
		if id1 != id2:
			dic = {row[1] : []}
	#add new value to key
	dic[row[1]].append(row[3]) # tag name is column 3, not 4
	count += 1
	date2 = row[4]
	id2 = row[1]
closeDBConnection(cursor)	 
closeDBConnection(cursorSS)