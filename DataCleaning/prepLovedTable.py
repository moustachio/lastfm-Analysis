"""
Converts raw loved tracks table to updated  table for analysis.
Converts all item_url strings to numeric item IDs
"""

cursor.execute("CREATE TABLE IF NOT EXISTS `lastfm_lovedtracks` ( \
  `user_id` INT(10), \
  `item_id` mediumint(8), \
  `love_time` TIMESTAMP, \
  UNIQUE INDEX `user_id_item_url` (`user_id`, `item_url`), \
  INDEX `item_url` (`item_url`), \
  INDEX `user_id` (`user_id`) \
) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
