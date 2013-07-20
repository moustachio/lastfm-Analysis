"""

Basic database conection methods.

Standard connection should always be "db".
Streaming connection should always be "dbSS"

"""

import MySQLdb
import MySQLdb.cursors

def closeDBConnection(cursor):
        db.commit()
        cursor.close()

def closeDBConnectionSS(cursor):
        dbSS.commit()
        cursor.close()
        

### These are the actual DB connection calls. 
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm")
dbSS = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root",db="analysis_lastfm",cursorclass=MySQLdb.cursors.SSCursor) 
