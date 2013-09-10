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
print 'taggers per month DONE'

### Annotations per month
cursor.execute("select tag_month, count(*) as freq from lastfm_annotations group by tag_month order by tag_month asc;")
result = cursor.fetchall()
out = open('../results/globalTaggingActivity/annotationsPerMonth','w')
for row in result:
	out.write(str(row[0])+'\t'+str(row[1])+'\n')
out.close()
print 'anno per month DONE'

### Annotations per item per month
cursor.execute("SELECT COUNT(*) / COUNT(DISTINCT item_id) as tag_average,tag_month FROM lastfm_annotations GROUP BY tag_month ORDER by tag_month asc")
result = cursor.fetchall()
out = open('../results/globalTaggingActivity/annoPerItemPerMonth','w')
for row in result:
	out.write(str(row[0])+'\t'+str(row[1])+'\n')
out.close()
print 'anno per item per month DONE'

closeDBConnection(cursor)