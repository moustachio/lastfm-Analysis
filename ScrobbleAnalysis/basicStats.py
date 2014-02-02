import cPickle
from dateutil.parser import parse

artistData = {}
monthData = {}

for line in open('d:/scrobble_sample.tsv'):
	line = line.strip().split('\t')
	uid = line[0]
	songURL = line[1].split('/')
	scrobble_time = parse(line[2])
	if songURL[0] == '+noredirect':
		songURL = songURL[1:]
	artist = songURL[0]
	data[artist] = data.get(artist,0)+1
	month = scrobble_time.month
	monthData[month] = monthData.get(month,0)+1

