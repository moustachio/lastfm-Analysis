"""
Methods for misc. distribution-level analyses
"""

import collections
import numpy as np

# Calculates thresholds between head, mid, and tail of a distribution, folowing Celma (2010)
def calcThresholds(data):
	volume = float(sum(data))    
	cumProp = 0
	found = False
	for index,i in enumerate(data):
		cumProp += i
		prop = cumProp / volume
		if not found and prop >= 0.5:
			headThreshold = int(round((index+1) ** (2.0/3.0)))
			midThreshold = int(round((index+1) ** (4.0/3.0)))
			found =True
		last = prop
	print "Head-Mid threshold: %s" % (headThreshold)
	print "Mid-Tail threshold: %s" % (midThreshold)
	print "Total in head, mid, tail, overall: %s, %s, %s, %s" % (headThreshold, midThreshold-headThreshold, len(data)-midThreshold, len(data))
	return headThreshold, midThreshold

# Entropy calculations. Calculates entropy and relative entropy, and also returns the total number and number of unique items in "li". If input is list, assumes each value is a unique itemID. If input is dict, assumes keys are item IDs and values are frequencies
def ent(li):
	if type(li) == list:
		counter=collections.Counter(li)
		freq = counter.values()
	if type(li) == dict:
		freq = li.values()
	# return zero if there's only one unique tag
	if len(freq)==1:
		return (0,0,1,freq[0])
	sm = sum(freq) 
	#replaces each value with the relative frequency
	for i,x in enumerate(freq):
		freq[i] = (x * 1.0) / sm
	e = 0
	#calc entropy
	for x in freq: 
		e += x * np.log2(x) 
	e = -e
	n = len(freq)
	p = 1.0/n
	eMax = - n*p*np.log2(p)
	return e , e / eMax , n , sm
	

# Calcualtes gini coefficent on a list of values, or dictionary of frequencies
def gini(li):
	if type(li)==list:
		li = collections.Counter(li).values()
	if type(li)==dict:
		li = li.values()
	n = float(len(li))
	numSum = 0 # sum from numerator
	for i, freq in enumerate(sorted(li)):
		numSum += ((i+1)*float(freq)) 
	return (2*numSum)/(n*sum(li)) - ((n+1)/n)

# Calculates gini coeffecient on distribution of frequencies X
# possible alternative to function above, need to do speed comparison
# Might have issues with negative results...DO NOT user for now
def calc_gini(dist): 
	x = sorted(dist) 
	n = len(dist)
	G = sum(xi * (i+1) for i,xi in enumerate(dist))
	G = 2.0*G/(n*sum(dist)) 
	return G - 1 - (1./n)
