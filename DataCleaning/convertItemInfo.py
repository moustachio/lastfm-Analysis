"""
Converts artist names in lastfm_itemlist to artist_ids for better indexing.
MUST BE RUN AFTER prepAnnoTable AND prepScrobble !!!
"""

import sys
sys.path.append('../bin')
import MySQLdb
import MySQLdb.cursors
import time


### Set up cursors
# streaming cursor, for reading full annotations table from raw database
dbSS = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm",cursorclass=MySQLdb.cursors.SSCursor) 
# standard curosr, for wirting to new analysis databsase
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")

# init cursors
cursorSS=dbSS.cursor()
cursor=db.cursor()

# update artist_id to equal item_id for all artists
cursor.execute("update lastfm_itemlist set artist_id=item_id where item_type='artist';")
db.commit()
print "artists updated"

artistDict = {}

# get all albums and songs into sreaeming cursor 
cursorSS.execute("select * from lastfm_itemlist where item_type = 'artist';") 

# get all our artist IDs in the dictionary
for row in cursorSS:
	artistName = row[2]
	artistDict[artistName] = row[0]
print "dictionary built"

# Now use the dictionary to update artist_id values for everything else
cursorSS.execute("select * from lastfm_itemlist where item_type != 'artist';")

count = 0
start = time.time()
for row in cursorSS:
	count += 1
	if count % 100000 == 0:
		now = time.time()-start
		print count, now
	itemID=row[0]
	artistName = row[2]
	artistID = artistDict.get(artistName)
	cursor.execute("update lastfm_itemlist set artist_id=%s where item_id=%s;",(artistID,itemID))

db.commit()
cursor.close()
dbSS.commit()
cursorSS.close()