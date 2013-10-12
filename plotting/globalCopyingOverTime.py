"""
Script to plot global pCopy measures over time.
"""

from matplotlib import pyplot, dates
import datetime


f = open('../Results/globalCopyValues')
f.readline() # clear headers

# converts date in format "yyyy-mm-dd" to days since epoch
def dateConvert(dateString):
	return dates.date2num(datetime.datetime.strptime(dateString,'%Y-%m-%d'))

x = []
top = []
bin = []
norm = []

for line in f:
	line = line.strip().split('\t')
	x.append(dateConvert(line[0]))
	top.append(float(line[1]))
	bin.append(float(line[2]))
	norm.append(float(line[3]))

pyplot.plot_date(x,top,ls='-',marker=None,c='red')
pyplot.plot_date(x,bin,ls='-',marker=None,c='green')
pyplot.plot_date(x,norm,ls='-',marker=None,c='blue')

pyplot.ylabel('Copy Index')

pyplot.show()