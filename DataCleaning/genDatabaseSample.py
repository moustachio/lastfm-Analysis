import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="mysql")

cursor=db.cursor();
cursor.execute("drop database if exists lastfm_mini;")
cursor.execute("create database lastfm_mini;")
db.commit()

cursor.execute("show tables from analysis_lastfm;")
tables = [i[0] for i in cursor.fetchall()]


for table in tables:
	cursor.execute("create table lastfm_mini."+table+" like analysis_lastfm."+table)
	cursor.execute("insert into lastfm_mini."+table+" select * from analysis_lastfm."+table+" limit 100000")
	db.commit()
	print "Table "+table+" complete"
cursor.close()

	