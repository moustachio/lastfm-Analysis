import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="crawler_lastfm")

users = []
count = 0

done = [int(i.strip()) for i in open('scrobble_sample_users.csv_1_2').readlines()]
log = open('scrobbleSamplerLog','w')

cursor=db.cursor()
for line in open('users.txt'):
	uid = int(float(line.strip().split('\t')[1]))
	if uid in done:
		print 'User '+str(uid)+' already done!'
	else:
		cursor.execute("select * from errorqueue_updated where user_id=%s",uid)
		if cursor.fetchall():
			print 'Error! Skipping user '+str(uid)
		else:
			print "no error, copying scrobbles for user "+str(uid)+", "+str(count)+" done so far"
			cursor.execute("select playcount from lastfm_users where user_id=%s",uid)
			listedPlayCount = cursor.fetchall()[0][0]
			cursor.execute("select count(*) from lastfm_scrobbles where user_id=%s",uid)
			scrobbleTableCount = cursor.fetchall()[0][0]
			cursor.execute("select user_name from lastfm_users where user_id=%s",uid)
			username = cursor.fetchall()[0][0]
			cursor.execute("select crawl_flag from lastfm_crawlqueue where user_name=%s",username)
			crawlFlag =  cursor.fetchall()[0][0]
			out = '\t'.join(map(str,[uid,username,listedPlayCount,scrobbleTableCount,crawlFlag]))
			print out
			log.write(out+'\n')
			if scrobbleTableCount > 0:
				count +=1 
				cursor.execute("insert into scrobble_sample select * from lastfm_scrobbles where user_id=%s", uid)
				db.commit()