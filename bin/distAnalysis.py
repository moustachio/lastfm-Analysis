#/usr/bin/python

"""
Methods for misc. distribution-level analyses
"""

# Calculates gini coeffecient on distribution of frequencies X
def calc_gini(dist): 
	x = sorted(dist) 
	n = len(dist)
	G = sum(xi * (i+1) for i,xi in enumerate(dist))
	G = 2.0*G/(n*sum(dist)) 
	return G - 1 - (1./n)

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