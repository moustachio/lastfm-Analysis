"""
Generates sorted frequency distributions for a few basic measures from the folksonomy.
Also generates basic plot of distributions of tag character and word counts.
"""

import sys 
sys.path.append('../bin')
from urllib2 import unquote
import cPickle
from matplotlib import pyplot as plt

### Built tag frequency dictionary

f = open('../Results/generalData/annotationsPerTag')

data = {}
flippedTagDict = cPickle.load(open('../DataCleaning/tagDict'))
tagDict = dict((value, key) for key, value in flippedTagDict.iteritems())

for line in f:
	line = line.strip().split('\t')
	tag_id = int(line[0])
	count = int(line[1])
	tagName = tagDict[int(tag_id)]
	raw = tagName
	tagName = unquote(tagName.replace('+',' '))
	data[tagName] = count

### Get character and word count lists
### _unique versions ignore frequency of tag use 

nCharList = [] 
nCharList_unique = []
nWordsList = []
nWordsList_unique = []
for tag in data:
	nChar = len(tag)
	nWords = len(tag.split())
	nCharList_unique.append(nChar)
	nWordsList_unique.append(nWords)
	nCharList += [nChar]*data[tag]
	nWordsList += [nWords]*data[tag]

### Generate plots (size and spacing still need to be adjusted)

fig = plt.figure()
plt.subplot(221)
plt.hist(nCharList_unique,bins=max(nCharList_unique),normed=True)
plt.xlim(0,60)
plt.xlabel('n characters')
plt.ylabel('Prob. Density')
plt.title('Unique tags')

plt.subplot(222)
plt.hist(nCharList,bins=max(nCharList_unique),normed=True)
plt.xlim(0,60)
plt.xlabel('n characters')
plt.ylabel('Prob. Density')
plt.title('All annotations')

plt.subplot(223)
plt.hist(nWordsList_unique,bins=max(nWordsList_unique),normed=True)
plt.xlim(0,20)
plt.xlabel('n words')
plt.ylabel('Prob. Density')

plt.subplot(224)
plt.hist(nWordsList,bins=max(nWordsList_unique),normed=True)
plt.xlim(0,20)
plt.xlabel('n words')
plt.ylabel('Prob. Density')

fig.savefig('../Plotting/charWordDists.pdf')
