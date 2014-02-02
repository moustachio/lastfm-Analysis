import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="crawler_lastfm")

users = [line.strip() for line in open('scrobble_sample_users.csv')]

out = open('d:/scrobble_sample.tsv','w')
cursor=db.cursor()
for user in users:
	print user
	cursor.execute("select * from scrobble_sample where user_id=%s order by scrobble_time asc;",user)
	result = cursor.fetchall()
	for scrobble in result:
		out.write('\t'.join([str(elem) for elem in scrobble])+'\n')
out.close()
cursor.close()