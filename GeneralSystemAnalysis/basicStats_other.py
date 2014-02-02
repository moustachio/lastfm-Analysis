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

### Friends per user
cursor.execute("select id, count(*) as freq from (select friend_id1 as id from friends_updated union all select friend_id2 as id from friends_updated) \
	as merged join lastfm_users on merged.id = lastfm_users.user_id group by id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'friendsPerUser')
print 'friendsPerUser done'

### Groups per user
cursor.execute("select user_id, count(*) as freq from groups_updated group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'groupsPerUser')
print 'groupsPerUser done'

### Members per group
cursor.execute("select group_name, count(*) as freq from groups_updated group by group_name order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'membersPerGroup')
print 'membersPerGroup done'

### Loved tracks per user
cursor.execute("select user_id, count(*) as freq from lastfm_lovedtracks group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'lovedPerUser')
print 'lovedPerUser done'

### Banned tracks per user
cursor.execute("select user_id, count(*) as freq from lastfm_bannedtracks group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'bannedPerUser')
print 'bannedPerUser done'
"""
### Scrobbles per item
cursor.execute("select item_id, count(*) as freq from lastfm_scrobbles group by item_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'scrobblesPerItem')
print 'scrobblesPerItem done'
"""
### Scrobbles per artist
cursor.execute("select artist_id, count(*) as freq from lastfm_scrobbles group by artist_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'scrobblesPerArtist')
print 'scrobblesPerArtist done'

### Scrobbles per user
cursor.execute("select user_id, count(*) as freq from lastfm_scrobbles group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'scrobblesPerUser')
print 'scrobblesPerUser done'

### Unique artists listened per user
cursor.execute("select user_id, count(distinct artist_id) as freq from lastfm_scrobbles group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueArtistsListenedPerUser')
print 'uniqueArtistsListenedPerUser done'

### Unique items listened per user
cursor.execute("select user_id, count(distinct item_id) as freq from lastfm_scrobbles group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueItemsListenedPerUser')
print 'uniqueItemsListenedPerUser done'

closeDBConnection(cursor)
