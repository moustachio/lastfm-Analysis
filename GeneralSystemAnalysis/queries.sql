/*
Misc. queries for generating .tsv files used by other analysis scripts (ideally where reading through a text file is quicker than querying DB)
*/


SELECT * FROM lastfm_annotations order by tag_month, item_id INTO OUTFILE 'anno_sort_date.iid_.tsv';

select tag_month, tag_id, count(*) as freq from lastfm_annotations group by tag_month,tag_id order by tag_month, tag_id INTO OUTFILE 'tagFreqByMonth.tsv';