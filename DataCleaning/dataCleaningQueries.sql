### Select scrobble data sample from users with complete data 
create table scrobble_sample like lastfm_scrobbles;
insert into scrobble_sample select * from lastfm_scrobbles t1 where not exists (select user_id from errorqueue_updated t2 where t1.user_id=t2.user_id);
create table scrobble_sample_updated like scrobble_sample;
insert into scrobble_sample_updated select scrobble_sample.* from scrobble_sample join lastfm_users on scrobble_sample.user_id=lastfm_users.user_id;

### Clean up friends table 
CREATE TABLE analysis_lastfm.`friends_updated` (
  `friend_id1` int NOT NULL,
  `friend_id2` int NOT NULL,
  PRIMARY KEY (`friend_id1`,`friend_id2`),
  KEY `friend_id1` (`friend_id1`),
  KEY `friend_id2` (`friend_id2`)
);
insert ignore into analysis_lastfm.friends_updated select crawler_lastfm.lastfm_friendlist.friend_id1, crawler_lastfm.lastfm_friendlist.friend_id2 from crawler_lastfm.lastfm_friendlist join analysis_lastfm.lastfm_users on (crawler_lastfm.lastfm_friendlist.friend_id1=analysis_lastfm.lastfm_users.user_id or crawler_lastfm.lastfm_friendlist.friend_id2=analysis_lastfm.lastfm_users.user_id);

### Clean up annotations table;
create table annotations_updated like lastfm_annotations;
insert into annotations_updated select lastfm_annotations.* from lastfm_annotations join lastfm_users on lastfm_annotations.user_id=lastfm_users.user_id;

### Clean up groups table;
create table groups_updated like lastfm_groups;
insert into groups_updated select lastfm_groups.* from lastfm_groups join lastfm_users on lastfm_groups.user_id=lastfm_users.user_id;

### Clean up bannedtrack table;
create table bannedtracks_updated like lastfm_bannedtracks;
insert into bannedtracks_updated select lastfm_bannedtracks.* from lastfm_bannedtracks join lastfm_users on lastfm_bannedtracks.user_id=lastfm_users.user_id;

### Clean up lovedtrack table;
create table lovedtracks_updated like lastfm_lovedtracks;
insert into lovedtracks_updated select lastfm_lovedtracks.* from lastfm_lovedtracks join lastfm_users on lastfm_lovedtracks.user_id=lastfm_users.user_id;


