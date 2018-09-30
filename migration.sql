CREATE TABLE IF NOT EXISTS `animal` (
  id integer primary key,
  name varchar(255)
);

CREATE TABLE IF NOT EXISTS `animal_schedule` (
  id integer primary key,
  `animal_id` integer(11),
  `time` varchar(5),
  `portions` integer(11)
);

CREATE TABLE IF NOT EXISTS `feed_history` (
  id integer primary key,
  `animal_id` integer(11),
  `time` varchar(5),
  `portions` integer(11),
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
);