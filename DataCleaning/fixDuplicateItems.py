# It seems the simplest way to find the duplicates is to just dump the itemlist to file
# Once we've done that...

import MySQLdb
import cPickle
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")

ddir = 'H:/MySQL/data/analysis_lastfm/analysis_db_2014.01.31/'

"""
#ddir = 'H:/BTSync/Research.Archive/LastFM/database_analysis_2014.01.31/'
ddir = 'H:/MySQL/data/analysis_lastfm/analysis_db_2014.01.31/'


f = open(ddir+'lastfm_itemlist.txt')
out = open(ddir+'itemDuplicates','w')
d = {}
for line in f:
	strp = line.strip().split('\t')
	url = strp[6]
	if url in d:
		print strp
		out.write(line)
	else:
		d[url] = None
out.close()
"""


d = cPickle.load(open('h:/Dropbox/Research/PROJECTS/Tagging/lastfm-analysis/dataCleaning/itemDict'))

print "dict loaded"

count = 0
cursor = db.cursor()
for line in open(ddir+'itemDuplicates'):
	line = line.strip().split('\t')
	url = line[-1]
	correctID = int(d[url])
	cursor.execute("select * from lastfm_itemlist where item_url=%s",url)
	result = cursor.fetchall()
	redundant = [i[0] for i in result if i[0] != correctID]
	if redundant:
		print correctID, redundant,len(url.split('/'))  ### OK, at least we know these are all artists, not albums or songs...

		for table in ('lastfm_scrobbles','lastfm_annotations','lastfm_lovedtracks','lastfm_bannedtracks'):
			for item in redundant:
				cursor.execute('select count(*) from '+table+' where item_id=%s',item)
				cnt = cursor.fetchall()[0][0]
				if cnt>0:
					print 'duplicates found in table '+table+' for item '+str(item)
					cursor.execute("update "+table+" set item_id=%s where item_id=%s",(correctID,item))
					cursor.execute("update "+table+" set artist_id=%s where item_id=%s",(correctID,item))
				else:
					print 'table '+table+' is good!'
				cursor.execute("delete from lastfm_itemlist where item_id=%s",item)
				#print "item "+str(item)+" deleted"
				count += 1
			db.commit()
print count