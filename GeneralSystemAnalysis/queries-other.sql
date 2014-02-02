### Tag self information data as .tsv
select * from tag_info order by tag_id, date into outfile 'tagInformation_tid_date.tsv';

### Entropy tables
select * from ent_users order by user_id, date into outfile 'ent_users.tsv'
select * from ent_items order by item_id, date into outfile 'ent_items.tsv'