import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")

cursor = db.cursor()
count = 0

for line in open('f:/MySQL/data/analysis_lastfm/users.txt'):
	uid = int(float(line.strip().split('\t')[1]))
	cursor.execute("select count(*) from lastfm_annotations where user_id=%s",uid)
	annoCount = cursor.fetchone()[0]
	cursor.execute("update lastfm_users set anno_count=%s where user_id=%s;",(annoCount,uid))
	if count % 100000 == 0:
		db.commit()
		print count
	count += 1
db.commit()
cursor.close()

