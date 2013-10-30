"""
Generates various plots of global activity over time
"""

import datetime
import itertools
from matplotlib import dates,pyplot

# plot coloring setup
colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
colors = itertools.cycle(colorList)

# converts date in format "yyyy-mm-dd" to days since epoch
def dateConvert(dateString):
	return dates.date2num(datetime.datetime.strptime(dateString,'%Y-%m-%d'))

# All months in dataset
allDates = [line.strip().split('\t')[0] for line in open('../Results/globalTaggingActivity/annotationsPerMonth').read().strip().split('\n')]
X = [dateConvert(i) for i in allDates]

# Trimming of months from beginning and end of distribution
start = 6
end = -8

X = X[start:end]


##############################
# Generates split-axis plot of annotations per month, taggers per month, and anno-per-tagger values per month, all on the same plot
##############################

# Annotations per month, taggers per month, and annotations per tagger per month
annoPerMonth = [int(line.strip().split('\t')[1]) for line in open('../Results/globalTaggingActivity/annotationsPerMonth').read().strip().split('\n')]
taggersPerMonth = [int(line.strip().split('\t')[1]) for line in open('../Results/globalTaggingActivity/taggersPerMonth').read().strip().split('\n')]
annoPerTagger = [j/float(taggersPerMonth[i]) for i,j in enumerate(annoPerMonth)]

f,(ax1,ax2,ax3) = pyplot.subplots(3,1,sharex=True)

for ax in (ax1,ax2,ax3):
	ax.plot_date(X,annoPerMonth[start:end],ls='-',marker=None,c='red',label='annotations')
	ax.plot_date(X,taggersPerMonth[start:end],ls='-',marker=None,c='green',label='active users')
	ax.plot_date(X,annoPerTagger[start:end],ls='-',marker=None,c='blue',label='anno. per user')
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

ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),ncol=3, fancybox=True, shadow=True)
f.savefig('plots/globalTaggingActivity.pdf')

##############################
# Global changes in entropy, relative entropy, gini coefficient, unique tags, and total annotations over time
##############################

# Format = 
# 0: date
# 1: entropy
# 2: relativeEntropy
# 3: gini
# 4: tags
# 5: annotations
# 6: annoPerTag
# 7: entropy.cumulative
# 8: relativeEntropy.cumulative
# 9 gini.cumulative
# 10: tags.cumulative
# 11: annotations.cumulative
# 12: annoPerTag.cumulative

f = open('../Results/entcetera')

colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
colors = itertools.cycle(colorList)

header = f.readline() # skip header
header = header.strip().split('\t')
data = {i:[] for i in range(len(header))}


for line in f:
	line = line.strip().split('\t')
	for i,val in enumerate(line):
		data[i].append(val)

### Everything that's 0-1 scaled, so rel.entropy and gini (cumulative and month-by-month)
fig = pyplot.figure()
for i in (2,3,8,9):
	pyplot.plot_date(X,data[i][start:end],label=header[i],ls='-',marker=None,color=colors.next())
pyplot.ylim(0.4,1)
pyplot.legend(loc='lower left')
fig.savefig('plots/diversityOverTime_folksonomy.pdf')

### Number of annotations and tags, and related
### THIS IS ALL SCRATCH FOR NOW

# Calculate the number of new tags added to the vocabulary each month
last = 0
newTags = []
oldTags = []
for i in data[10]:
	i = int(i)
	newTags.append(i-last)
	last = i

fig = pyplot.figure()
for i in (6,12):
	pyplot.plot_date(X,data[i][start:end],label=header[i],ls='-',marker=None,color=colors.next())
pyplot.plot_date(X,newTags[start:end],label='new tags',ls='-',marker=None,color=colors.next())
#pyplot.ylim(0.4,1)
pyplot.legend(loc='upper left')
fig.savefig('plots/tagsOverTime_folksonomy.pdf')