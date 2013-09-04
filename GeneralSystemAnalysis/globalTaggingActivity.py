"""
Calculates general tagging trends over time.
"""

import sys 
sys.path.append('../bin')
from dbSetup import *
cursor = db.cursor()

### Unique taggers per month
cursor.execute("select tag_month, count(distinct user_id) as freq from lastfm_annotations group by tag_month order by tag_month asc;")
result = cursor.fetchall()
out = open('../results/globalTaggingActivity/taggersPerMonth','w')
for row in result:
	out.write(str(row[0])+'\t'+str(row[1])+'\n')
out.close()

### Annotations per month
cursor.execute("select tag_month, count(*) as freq from lastfm_annotations group by tag_month order by tag_month asc;")
result = cursor.fetchall()
out = open('../results/globalTaggingActivity/annotationsPerMonth','w')
for row in result:
	out.write(str(row[0])+'\t'+str(row[1])+'\n')
out.close()

closeDBConnection(cursor)