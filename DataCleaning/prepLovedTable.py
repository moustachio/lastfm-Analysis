"""
Converts raw loved tracks table to updated  table for analysis.
Converts all item_url strings to numeric item IDs
"""

import sys
sys.path.append('../bin')
import dbMethods
import MySQLdb
import MySQLdb.cursors
import time
import cPickle    

# streaming cursor, for reading full annotations table from raw database
#dbSS = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm",cursorclass=MySQLdb.cursors.SSCursor) 
# standard curosr, for wirting to new analysis databsase
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")

#cursorSS=dbSS.cursor()
#cursorSS.execute("select * from lovedtracks_updated;") # get all loved_tracks on streming cursor
cursor=db.cursor()

cursor.execute('DROP TABLE IF EXISTS `lastfm_lovedtracks`;')
cursor.execute("CREATE TABLE `lastfm_lovedtracks` ( \
	`user_id` int NOT NULL, \
	`item_id` int NOT NULL, \
	`artist_id` int NOT NULL, \
	`love_time` TIMESTAMP NOT NULL, \
	UNIQUE INDEX `user_id_item_id` (`user_id`, `item_id`), \
	INDEX `item_id` (`item_id`), \
	INDEX `artist_id` (`artist_id`), \
	INDEX `user_id` (`user_id`), \
	INDEX `love_time` (`love_time`) \
) \
COLLATE='latin1_swedish_ci' \
ENGINE=InnoDB;")

try:
	itemDict = cPickle.load(open('itemDict'))
except:
	itemDict = {} 


# just for feedback on the script's progress
count = 0 
startTime = time.time()

for row in open('f:/MySQL/data/analysis_lastfm/lovedtracks_updated.tsv'):
	row = row.strip().split('\t')

	if count > 0:
		if count % 100000 == 0: # Every 100,000 rows, printout progress so far
			minSinceStart = (time.time() - startTime) / 60.0
			print count, minSinceStart, minSinceStart / (count/100000)
			if count % 1000000 == 0: # every million rows, commit new rows to analysis database
				db.commit()

	itemURL = row[1].strip().lower()
	spl = itemURL.split('/')
	if spl[0]=='+noredirect':
		artistName = spl[1]
		itemURL = '/'.join(spl[1:])
	else:
		artistName = spl[0]

	itemID = itemDict.get(itemURL)
	artistID = itemDict.get(artistName)
	
	
	# If the IDs aren't in the dict, add to DB
	if not artistID:
		artistID = dbMethods.itemIDfromURL(artistName,check=True)
		itemDict[artistName] = artistID
	if not itemID:
		if artistName==itemURL:
			itemID = artistID
		else:
			itemID = dbMethods.itemIDfromURL(itemURL,check=True)
			itemDict[itemURL] = itemID

	# insert row and increment count
	cursor.execute("insert ignore into lastfm_lovedtracks (user_id,item_id,artist_id,love_time) values (%s,%s,%s,%s)",(row[0],itemID,artistID,row[2]))
	count += 1 # total rows done so far

# Clean up everything and write item/tag dictionaries to file
db.commit()
cursor.close() 
cPickle.dump(itemDict, open('itemDict','w'))