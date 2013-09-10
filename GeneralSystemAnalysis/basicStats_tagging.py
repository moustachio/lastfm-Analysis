#/usr/bin/python

"""
Generates sorted frequency distributions for a few basic measures from the folksonomy.
"""

import sys 
sys.path.append('../bin')
from dbSetup import *

def sortSaveData(data, filename):
	out = open('../results/generalData/'+filename,'w')
	for i in data:
		out.write(str(i[0])+'\t'+str(i[1])+'\n')

cursor=db.cursor()

### Annotations per user
cursor.execute("select user_id, count(*) as freq from lastfm_annotations group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'annotationsPerUser')
print 'annotationsPerUser done'

### Annotations per item
cursor.execute("select item_id, count(*) as freq from lastfm_annotations group by item_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'annotationsPerItem')
print 'annotationsPerItem done'

### Annotations per tag
cursor.execute("select tag_id, count(*) as freq from lastfm_annotations group by tag_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'annotationsPerTag')
print 'annotationsPerTag done'

### Unique tags per user
cursor.execute("select user_id, count(distinct tag_id) as freq from lastfm_annotations group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueTagsPerUser')
print 'uniqueTagsPerUser done'

### Unique items annotated per tag
cursor.execute("select tag_id, count(distinct item_id) as freq from lastfm_annotations group by tag_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueItemsPerTag')
print 'uniqueItemsPerTag done'

### Unique tags per item
cursor.execute("select item_id, count(distinct tag_id) as freq from lastfm_annotations group by item_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueTagsPerItem')
print 'uniqueTagsPerItem done'

### Unique items tagged by each user
cursor.execute("select user_id, count(distinct item_id) as freq from lastfm_annotations group by user_id order by freq desc;")
result = cursor.fetchall()
sortSaveData(result,'uniqueItemsPerUser')
print 'uniqueItemsPerUser done'

### Histogram data of the number of instances in which a user assigned N unique tags to a given item (i.e. in most cases a user assigns one tag to any given item)
cursor.execute("select freq,count(*) from (select count(*) as freq from lastfm_annotations group by user_id,item_id) dt group by freq order by freq asc;")
result = cursor.fetchall()
sortSaveData(result,'tagAssignmentHist')
print 'tagAssignmentHist done'

closeDBConnection(cursor)
