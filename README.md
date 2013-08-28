Last.fm Analysis scripts
========================

Assorted scripts for analysis of tagging and listening data crawled from Last.fm.

bin
---

Contains misc support methods, principally for database interaction

* dbMethods.py:	Misc. support methods for interacting with the database.
* dbSetup.py: Basic database conection methods.

DataCleaning
------------

Scripts for cleaning and prepping raw data for analysis

*For these scripts, run sequence matters!*

1. prepAnnoTable.py: Converts raw annotations table to analysis-ready version

2. prepScrobbleTable.py: Converts raw scrobbles table to analysis-ready version

3. convertItemInfo.py: Converts artist names to artist IDs in lastfm_itemlist

EntropyAnalysis
---------------

Scripts for calculating diversity of tags by item, user, etc.

* calcEntropyByItem.py: Calculates entropy metrics over time for all items

Plotting
--------

Scripts for data visualization

ImitationAnalysis
-----------------

Scripts for analyzing imitation behavior in users' tagging habits
