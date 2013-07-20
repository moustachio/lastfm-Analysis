/*
Sets up analysis database, copying tables from raw database. Also adds relevant indexes. Scrobble and annotation tables are more complex, and are handled separately.
*/

SET autocommit=0;

### Create main database
drop database if exists analysis_lastfm;
create database analysis_lastfm;

use analysis_lastfm;

### copy 'as-is' tables 
#create table analysis_lastfm.lastfm_extended_user_info like crawler_lastfm.lastfm_extended_user_info;
CREATE TABLE IF NOT EXISTS `lastfm_extended_user_info` (
  `user_name` varchar(100) NOT NULL,
  `user_id` int(10) NOT NULL,
  `country` varchar(2) DEFAULT NULL,
  `age` tinyint(3) UNSIGNED DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `subscriber` tinyint(1) UNSIGNED DEFAULT NULL,
  `playcount` int(10) SIGNED DEFAULT NULL,
  `playlists` smallint(5) UNSIGNED DEFAULT NULL,
  `bootstrap` tinyint(1) UNSIGNED DEFAULT NULL,
  `registered` datetime DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `anno_count` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  INDEX (user_name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into lastfm_extended_user_info select * from crawler_lastfm.lastfm_extended_user_info;
COMMIT;

CREATE TABLE IF NOT EXISTS `lastfm_userlist` (
  `user_id` int(10) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX  (user_name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into lastfm_userlist select * from crawler_lastfm.lastfm_userlist;
COMMIT;

CREATE TABLE IF NOT EXISTS `lastfm_friendlist` (
  `friend_id1` int(10) NOT NULL,
  `friend_id2` int(10) NOT NULL,
  `sanity_check_id` varchar(21) NOT NULL,
  PRIMARY KEY (`sanity_check_id`),
  INDEX (friend_id1),
  INDEX (friend_id2)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into lastfm_friendlist select * from crawler_lastfm.lastfm_friendlist;
COMMIT;

CREATE TABLE `entropy` (
  `item_id` MEDIUMINT(8) UNSIGNED NULL DEFAULT NULL,
  `tag_id` MEDIUMINT(8) UNSIGNED NULL DEFAULT NULL,
  `H` FLOAT NULL DEFAULT NULL,
  `J` FLOAT NULL DEFAULT NULL,
  `G` FLOAT NULL DEFAULT NULL,
  INDEX `item_id` (`item_id`),
  INDEX `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

COMMIT;
