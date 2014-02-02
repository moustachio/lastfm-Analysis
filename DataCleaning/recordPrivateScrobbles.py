import MySQLdb
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")


"""
This is the query to get all the user_ids we've found (so far) with private listening histories:

select user_id from (select * from lastfm_errorqueue union select * from errorqueue_updated) everything where retry_count=403; 

"""

cursor = db.cursor()
for line in open('private_2014.01.16.csv'):
	uid = line.strip()
	cursor.execute("update lastfm_users set scrobbles_private=1 where user_id=%s",uid)
db.commit()
cursor.close()
