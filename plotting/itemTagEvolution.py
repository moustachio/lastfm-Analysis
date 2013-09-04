from matplotlib import pyplot
from matplotlib import dates
from matplotlib import cm
import itertools
import sys 
sys.path.append('../bin')
from dbSetup import *
import numpy
from collections import Counter

colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
colors = itertools.cycle(colorList)
nTop = len(colorList)


anno=None
artistName = raw_input('ArtistName? ')
cursor = db.cursor()
cursor.execute("select item_id from lastfm_itemlist where item_type='artist' and artist=%s limit 1;",('+'.join(artistName.strip().lower().split())))
artistID = cursor.fetchone()[0]
print artistID
cursor.execute("select tag_id, count(*) as freq from lastfm_annotations where item_id=%s group by tag_id order by freq desc;", (artistID))
tags= cursor.fetchall()

fig = pyplot.figure()
ax = fig.add_subplot(111)
topCount = 0
for tag in tags:
	tag = tag[0]
	cursor.execute("select tag_month, count(*) from lastfm_annotations where item_id=%s and tag_id=%s group by tag_month;", (artistID,tag))
	anno = cursor.fetchall()
	if topCount < nTop:
		cursor.execute("select tag_name from lastfm_taglist where tag_id=%s;",(tag))
		label = cursor.fetchone()[0].replace('+',' ')
		topCount += 1
	else:
		label = None
	x = []
	y = []
	cumfreq=0
	for i in anno:
		date = i[0]
		cumfreq = cumfreq +int(i[1])
		x.append(dates.date2num(i[0]))
		y.append(cumfreq)
	ax.plot_date(x,y,ls='-',marker=None,c=colors.next(),label=label)
pyplot.legend(loc=2)
fig.savefig(artistName+'.pdf')