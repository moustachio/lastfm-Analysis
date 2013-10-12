"""
Converts raw annotations table to updated annotations table for analysis.
Converts all tag_name strings to numeric tag_id values, and item_url strings to numeric item IDs
"""

import sys
sys.path.append('../bin')
import dbMethods
import MySQLdb
import MySQLdb.cursors
import time
import cPickle    

### Set up cursors
# streaming cursor, for reading full annotations table from raw database
dbSS = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="crawler_lastfm",cursorclass=MySQLdb.cursors.SSCursor) 
# standard curosr, for wirting to new analysis databsase
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")

# Drop old tables (if they exist)
cursor=db.cursor()

cursor.execute("DROP TABLE IF EXISTS lastfm_annotations;")
cursor.execute("DROP TABLE IF EXISTS lastfm_taglist;")
cursor.execute("DROP TABLE IF EXISTS lastfm_itemlist;")
print "tables dropped"

# Set up new Tables  (REMOVED TAG_DATE!)
cursor.execute("CREATE TABLE lastfm_annotations ( \
	user_id int(10) unsigned NOT NULL, \
	item_id mediumint(8) unsigned NOT NULL, \
	artist_id mediumint(8) unsigned NOT NULL, \
	tag_id mediumint(8) unsigned NOT NULL, \
	tag_month date NOT NULL, \
	PRIMARY KEY (user_id,item_id,tag_id), \
	index item_id (item_id), \
	index tag_id (tag_id), \
	index tag_month (tag_month), \
	index artist_id (artist_id) \
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;") 

cursor.execute("CREATE TABLE lastfm_taglist ( \
	tag_id mediumint(8) unsigned NOT NULL AUTO_INCREMENT, \
	tag_name VARCHAR(255) NOT NULL, \
	PRIMARY KEY (tag_id), \
	index tag_name (tag_name) \
	) ENGINE=innodb DEFAULT CHARSET=latin1;") 

cursor.execute("CREATE TABLE lastfm_itemlist ( \
	item_id mediumint(8) NOT NULL AUTO_INCREMENT, \
	item_type VARCHAR(6), \
	artist VARCHAR(767), \
	artist_id mediumint(8), \
	album VARCHAR(767), \
	song VARCHAR(767), \
	item_url VARCHAR(767) NOT NULL, \
	PRIMARY KEY (item_id), \
	index artist_id (artist_id), \
	index item_url (item_url), \
	index item_type (item_type), \
	index artist (artist), \
	index album (album), \
	index song (song) \
	) ENGINE=innodb DEFAULT CHARSET=latin1;") 

db.commit()
cursor.close()

print "New tables set up"

# Dictionaries for storing itemID/itemURL and tagID/tagName relationships. Load them from file if they're already present (this should speed things up on subsequeent runs)
try:
	tagDict = cPickle.load(open('tagDict'))
except:
	tagDict = {} 
try:

	itemDict = cPickle.load(open('itemDict'))
except:
	itemDict = {} 

cursorSS=dbSS.cursor()
cursorSS.execute("select * from lastfm_annotations;") # get all annotations on streming cursor
cursor=db.cursor()

# just for feedback on the script's progress
count = 0 
startTime = time.time()

for row in cursorSS:

	if count > 0:
		if count % 100000 == 0: # Every 100,000 rows, printout progress so far
			minSinceStart = (time.time() - startTime) / 60.0
			print count, minSinceStart, minSinceStart / (count/100000)
			if count % 1000000 == 0: # every million rows, commit new rows to analysis database
				db.commit()

	# get tag and item IDs from dicts (if they're presnent)
	tagName = row[2].strip().lower()
	tagID = tagDict.get(tagName)
	itemURL = row[1].strip().lower()
	itemID = itemDict.get(itemURL)
	artistName = itemURL.split('/')[0]
	artistID = itemDict.get(artistName)
	
	fulldate = row[3]
	if not fulldate:
		# this captures the error we had for annotations from January 2013
		fulldate = "2013-01-01" 
	else:
		# set month to first of the month, to play nice between Python (datetime, doesn't allow zeros in dates) and MySQL
		month = fulldate.strftime('%Y-%m-01')
	
	# If the IDs aren't in the dicts, add to DB
	if not tagID:
		tagID = dbMethods.tagIDfromName(tagName,check=False)
		tagDict[tagName]=tagID
	if not artistID:
		artistID = dbMethods.itemIDfromURL(artistName,check=False)
		itemDict[artistName] = artistID
	if not itemID:
		if artistName==itemURL:
			itemID = artistID
		else:
			itemID = dbMethods.itemIDfromURL(itemURL,check=False)
			itemDict[itemURL] = itemID

	# insert row and increment count
	cursor.execute("insert ignore into lastfm_annotations (user_id,item_id,artist_id,tag_id,tag_month) values (%s,%s,%s,%s,%s)",(row[0],itemID,artistID,tagID,month))
	count += 1 # total rows done so far

# Clean up everything and write item/tag dictionaries to file
db.commit()
dbSS.commit()
cursor.close()
cursorSS.close()             
cPickle.dump(itemDict, open('itemDict','w'))
cPickle.dump(tagDict, open('tagDict','w'))
