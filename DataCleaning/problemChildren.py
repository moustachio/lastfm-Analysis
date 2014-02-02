"""

Script to delete a specific set of problematic users from all tables

SQL queries:

create table crawlqueue_updated like lastfm_crawlqueue;
insert into crawlqueue_updated select lastfm_crawlqueue.* from lastfm_crawlqueue join lastfm_users on lastfm_crawlqueue.user_name = lastfm_users.user_name;
select user_name from crawlqueue_updated where crawl_flag in 1,2,22; ### This gets us the actual problem children
"""

import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")
import sys

cursor=db.cursor()
user_ids = []

#f = open('H:/Dropbox/problemChildren.csv')
f = open('H:/Dropbox/problemChildren.csv')
for line in f:
	user_name = line.strip()
	cursor.execute("select user_id from lastfm_users where user_name=%s",user_name)
	user_id = cursor.fetchone()[0]
	user_ids.append(user_id)
	print user_name,user_id

	for table in ('groups_updated','lastfm_annotations','lastfm_bannedtracks','lastfm_lovedtracks','lastfm_scrobbles','lastfm_users'):
		n = cursor.execute("delete from "+table+" where user_id=%s",user_id)
		#cursor.execute("select row_count();")
		print table+': '+str(n)+' rows deleted'
		db.commit()
	print '------------------------------'

out = open('H:/Dropbox/problem_children_ids','w')
for u in user_ids:
	out.write(str(u)'\n')
out.close()


cursor.execute("select user_id from lastfm_users;")
allUsers = [i[0] for i in cursor.fetchall()]

print len(allUsers)

for user_id in [int(line.strip()) for line in open('H:/Dropbox/problem_children_ids')]:
	cursor.execute("select * from friends_updated where friend_id1=%s or friend_id2=%s",(user_id,user_id))
	count = 0
	result = cursor.fetchall()
	for row in result:
		fr1,fr2 = row[0],row[1]
		if fr1==user_id:
			check = fr2
		elif fr2==user_id:
			check = fr1
		else:
			print 'we have an issue with user '+str(user_id)
		if check not in allUsers:
			cursor.execute("delete from friends_updated where friend_id1=%s and friend_id2=%s",(fr1,fr2))
			count += 1
	print str(user_id)+': '+str(count)+' rows deleted'
	db.commit()
