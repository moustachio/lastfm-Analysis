import sys
sys.path.append('../bin')
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="mysql")

cursor=db.cursor();
cursor.execute("drop database if exists sample_lastfm;")
cursor.execute("create database sample_lastfm;")
db.commit()

cursor=db.cursor()
for dbName in ('annotations','bannedtracks','extended_user_info','friendlist','groups','lovedtracks'): # 'crawlqueue','errorqueue'
	cursor.execute("create table sample_lastfm.lastfm_"+dbName+" like crawler_lastfm.lastfm_"+dbName)
	cursor.execute("insert into sample_lastfm.lastfm_"+dbName+" select * from crawler_lastfm.lastfm_"+dbName+" limit 100000")
	db.commit()
cursor.close()

	