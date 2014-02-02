### Full annotation dataset as tsv (different sort otders)
select * from lastfm_annotations order by tag_month, item_id, tag_id into outfile 'annotations_date-iid-tid.tsv';
select * from lastfm_annotations order by item_id, tag_month, user_id, tag_id into outfile 'annotations_iid-date-uid-tid.tsv';

### Month by month tag usage frequencies (global)
select tag_month, tag_id, count(*) as freq from lastfm_annotations group by tag_month,tag_id order by tag_month, tag_id INTO OUTFILE 'tagFreqByMonth.tsv';