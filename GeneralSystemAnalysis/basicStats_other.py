#/usr/bin/python

"""
Generates sorted frequency distributions for a few basic measures from the folksonomy.
"""

import sys 
sys.path.append('../bin')
from dbSetup import *

def sortSaveData(data, filename):
	out = open('../results/generalData/'+filename,'w')
	for i in data:
		out.write(str(i[0])+'\t'+str(i[1])+'\n')

cursor=db.cursor()

### Scrobbles per item
cursor.execute("select item_id, count(*) as freq from lastfm_scrobbles group by item_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'scrobblesPerItem')
print 'scrobblesPerItem done'

### Scrobbles per user
cursor.execute("select user_id, count(*) as freq from lastfm_scrobbles group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'scrobblesPerUser')
print 'scrobblesPerUser done'

### Friends per user
cursor.execute("select id, count(*) as freq from (select friend_id1 as id from lastfm_friendlist union all select friend_id2 as id from lastfm_friendlist) as merged group by id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'friendsPerUser')
print 'friendsPerUser done'

closeDBConnection(cursor)
