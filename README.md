Last.fm Analysis scripts
========================

Assorted scripts for analysis of tagging and listening data crawled from Last.fm.

bin
---

Contains misc support methods, principally for database interaction

* dbMethods.py:	Misc. support methods for interacting with the database.
* dbSetup.py: Basic database conection methods.
* distAnalysis.py: Support methods for analysis of frequency distributions.

DataCleaning
------------

Scripts for cleaning and prepping raw data for analysis

*For these scripts, run sequence matters!*

1. dbPrep.sql: Generates analysis database and copies "as-is" tables that don't require immediate post-processing.
2. prepAnnoTable.py: Converts raw annotations table to analysis-ready version
3. prepScrobbleTable.py: Converts raw scrobbles table to analysis-ready version
4. prepLovedTable.py: Converts raw loved track table to analysis-ready version *INCOMPLETE*
5. convertItemInfo.py: Converts artist names to artist IDs in lastfm_itemlist

EntropyAnalysis
---------------

Scripts for calculating diversity of tags by item, user, etc.

* calcEntropyByItem.py: Calculates entropy metrics over time for all items. Also calculates number of unique/total annotations for each item for each month, and also used for recording pCopy values.
* calcEntropyGlobal.py: Calculates entropy and related measures across the full folksonomy for every month. *requires annotations_date-iid-tid.tsv (generated by queries.sql)*
* tagInformation.py: Calculates self-information of each tag in each month, and records in new DB table. *requires tagFreqByMonth.tsv (generated by queries.sql)*

GeneralSystemAnalysis
---------------------

Scripts for calculating high-level statistics of the full folksonomy and related measures.

* basicStats_other.py: Generates sorted frequency distributions (and related) for non-tagging measures (e.g. scrobbles per user, friends per user)
* basicStats_tagging.py: Generates sorted frequency distributions for a few basic measures from the folksonomy (tagging activity ONLY).
* globalTaggingActivity.py: Calculates general tagging trends over time. 
* queries.sql: Misc. queries for generating .tsv files used by other analysis scripts

ImitationAnalysis
-----------------

Scripts for analyzing imitation behavior in users' tagging habits

* pCopyByItem.py: Calculates probability of an existing tag being copied from month to month. E.g. probability that any given tag used at t+1 is copied from the tag distribution at time t. Calculation is performed on an item by item basis. *Requires table generated by calcEntropyByItem.py*
* pCopyGlobal: Calculates copying metrics pooled across the full folksonomy. These metrics are questionable and need revision.

Plotting
--------

Scripts for data visualization

* copyingVersusDiversity_heatmap.py: Generates heatmap plots of copy probability as a function of item entropy, pooled across all items.
* copyingVersusDiversity_lineplot.py: Generates line plots of copy probability as a function of item entropy, pooled across all items and showing average trends. *INCOMPLETE*
* full/full_plot.py: Calculates the average entropy, relative entropy, and gini coefficient as a function of item "age", across all items. The "age" of an item is defined as the number of calendar months since the first month in which it was tagged. *should be combined!*
* itemTagEvolution.py: Takes artist name as input and generates plot of cumulative frequencies of tags assigned to that artist over time. *INCOMPLETE*
* shrink/shrink_plot.py: calculates the entropy, relative entropy, and gini coefficient as a function of item age. The "age" of an item is defined as the number of months in which it has received tags since the first month in which it was tagged. *should be combined!*
* globalActivity.py: Generates various plots of global tagging activity over time.
* systemTagEvolution.py: Goal is to generate plots similar to itemTagEvolution.py, but for the full taxonomy. Just a placeholder filefor now *INCOMPLETE*


