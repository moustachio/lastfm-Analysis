"""
Script for calculating entropy measures across all time for all items in the annotation dataset.

Calculates entropy measure for tag distributuions of all unique items for each month in which those items received annotations.
"""

import sys 
sys.path.append('../bin') # This makes sure Python can see the 'bin' directory where dbSetup is located
from dbSetup import *
import collections
import numpy as np

cursor=db.cursor()
cursor.execute("DROP TABLE IF EXISTS ent_table;") # This should just drop the entropy table
# Variety of changes to fix the table creation call. The entropy values and such should be flots, like in Python (VARCHAR is for strings)
# Also don't want a primary key on this table (I can explain more about primary keys and indexes later), nor should we have indexes on float values
cursor.execute("CREATE TABLE ent_table (item_id mediumint(8) unsigned, month date, ent FLOAT, rel_ent FLOAT, gini FLOAT, \
	index(item_id), index(month)) ENGINE=innodb DEFAULT CHARSET=latin1;") 
closeDBConnection(cursor) # This calls both db.commit() and cursor.close(), so it's simpler to just use this

cursor=db.cursor()
cursorSS=dbSS.cursor()
cursorSS.execute("select * from anno_sample order by item_id, tag_month;") # anno_sample just for testing


#calculation of entropy and relative entropy. returns tuple
def ent(li):
	counter=collections.Counter(li)
	freq = counter.values()
	# just return zero if there's only one unique tag
	if len(freq)==1:
		return (0,0)
	sm = sum(freq) # shorter way to get total frequency
	#replaces each value with the relative frequency
	#changed to use "enumerate", which saves you from needing to define the "count" variable
	for i,x in enumerate(freq):
		freq[i] = (x * 1.0) / sm
	e = 0
	#calc entropy
	for x in freq: 
		e += x * np.log2(x) # negative only goes on at the end
	e = -e
	# Max possible entropy is the entropy if each unique tag were used an equal number of times. So this should be:
	n = len(freq)
	p = 1.0/n
	eMax = - n*p*np.log2(p)
	return e , e / eMax

		
def gini(li):
	 n = float(len(li))
	 numSum = 0 # sum from numerator
	 for i, freq in enumerate(sorted(li)):
		  numSum += ((i+1)*float(freq)) # need to change this to float, or we get zero for everything
	 return (2*numSum)/(n*sum(li)) - ((n+1)/n)


dic = {}
#new date and id
date1 = 0
id1 = 0
#old date and id
date2 = 0
id2 = 0
count = 0
for row in cursorSS:
	# this is just an efficiency thing. The code will be really slow if we commit every row. This way we only commit every 100,000 rows we've generated
	if count>0 and count % 100000:
		db.commit()
	date1 = row[4]
	id1 = row[1]
	#used when new item
	if not dic:
		dic = {row[1] : []} 
	#used when new month. calc ent rel_ent and gini and put them in db
	if (date1 != date2 or id1 != id2) and count > 0: # need to check if we've come to a new item, too
		#ent / rel ent tuple
		en = ent(dic[id2])
		e = en[0]
		re = en[1]
		gin = gini(dic[id2])
		cursor.execute("insert ignore into ent_table (item_id, month, ent, rel_ent, gini) values (%s,%s,%s,%s,%s)",(id2,date2,e,re,gin)) # names need to match what you defined in the table above
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
	
