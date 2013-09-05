"""
Generates various plots of global activity over time
"""


import datetime
import itertools
from matplotlib import dates,pyplot

# plot coloring setup
colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
colors = itertools.cycle(colorList)

# converts date in format "yyyy-mm-dd" to seconds since epoch
def dateConvert(dateString):
	return dates.date2num(datetime.datetime.strptime(dateString,'%Y-%m-%d'))

# All months in dataset
X = [dateConvert(line.strip().split('\t')[0]) for line in open('../Results/globalTaggingActivity/annotationsPerMonth').read().strip().split('\n')]

# Annotations per month, taggers per month, and annotations per tagger per month
annoPerMonth = [int(line.strip().split('\t')[1]) for line in open('../Results/globalTaggingActivity/annotationsPerMonth').read().strip().split('\n')]
taggersPerMonth = [int(line.strip().split('\t')[1]) for line in open('../Results/globalTaggingActivity/taggersPerMonth').read().strip().split('\n')]
annoPerTagger = [j/float(taggersPerMonth[i]) for i,j in enumerate(annoPerMonth)]

f,(ax1,ax2,ax3) = pyplot.subplots(3,1,sharex=True)

for ax in (ax1,ax2,ax3):
	ax.plot_date(X,annoPerMonth,ls='-',marker=None,c='red',label='annotations')
	ax.plot_date(X,taggersPerMonth,ls='-',marker=None,c='green',label='active users')
	ax.plot_date(X,annoPerTagger,ls='-',marker=None,c='blue',label='anno. per user')
ax1.set_ylim(100000,1100000)
ax2.set_ylim(500,50000)
ax3.set_ylim(0,70)

ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax3.spines['top'].set_visible(False)
pyplot.subplots_adjust(hspace=0.05)
ax1.xaxis.tick_top()
ax2.tick_params(axis='x',bottom='off',top='off') # don't put tick labels at the top
ax3.xaxis.tick_bottom()


d = .015 # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d,+d),(-d,+d), **kwargs)      # top-left diagonal
ax1.plot((1-d,1+d),(-d,+d), **kwargs)    # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d,+d),(1-d,1+d), **kwargs)   # bottom-left diagonal
ax2.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-right diagonal
ax2.plot((-d,+d),(-d,+d), **kwargs)      # top-left diagonal
ax2.plot((1-d,1+d),(-d,+d), **kwargs)    # top-right diagonal

kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
ax3.plot((-d,+d),(1-d,1+d), **kwargs)   # bottom-left diagonal
ax3.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-right diagonal

#pyplot.legend(loc=2)
#pyplot.legend(loc="upper left", bbox_to_anchor=(1,1))
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),ncol=3, fancybox=True, shadow=True)
#pyplot.show()
f.savefig('globalTaggingActivity.pdf')