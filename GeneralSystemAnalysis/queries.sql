/*
Misc. queries for generating .tsv files used by other analysis scripts (ideally where reading through a text file is quicker than querying DB)
*/


### Full annotation dataset as tsv 
SELECT * FROM lastfm_annotations order by tag_month, item_id INTO OUTFILE 'anno_sort_date.iid_.tsv';

### Month by month tag usage frequencies (global)
select tag_month, tag_id, count(*) as freq from lastfm_annotations group by tag_month,tag_id order by tag_month, tag_id INTO OUTFILE 'tagFreqByMonth.tsv';

### Tag self information data as .tsv
select * from tag_info order by tag_id, date into outfile 'tagInformation_tid_date.tsv';