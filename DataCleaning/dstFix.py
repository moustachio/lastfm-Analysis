# Fixes "impossible" times caused by DST errors (i.e. times between 2 and 3 am on these dates couldn't happen). These times are throwing errors on MySQL import, so we need to fix it in the raw data files.

# This version is formatted for lastfm_bannedtracks.txt - need to reformat for other tables, or else make a generalized version.

import sys

dstStartDates = ('2005-3-13','2006-03-12','2007-03-11','2008-03-09','2009-03-08','2010-03-14','2011-03-13','2012-03-11','2013-03-10')


for line in sys.stdin:
	spl = line.strip().split('\t')
	dt = spl[3]
	dtSpl = dt.split()
	if dtSpl[0] in dstStartDates and dtSpl[1].split(':')[0] == '02':
		sys.stdout.write('\t'.join(spl[:-1]+[dt[:11]+'03'+dt[13:],])+'\n')
	else:
		sys.stdout.write(line)


"""
From: http://aa.usno.navy.mil/faq/docs/daylight_time.php
2006 April 2	October 29
2007 *	March 11	November 4
2008	March 9	November 2
2009	March 8	November 1
2010	March 14	November 7
2011	March 13	November 6
2012	March 11	November 4
2013	March 10	November 3
2014	March 9	November 2
2015	March 8	November 1
2016	March 13	November 6
2017	March 12	November 5
2018	March 11	November 4
2019	March 10	November 3
2020	March 8	November 1
"""