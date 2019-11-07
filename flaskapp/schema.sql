DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS poll;

CREATE TABLE `author` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`username`	TEXT NOT NULL,
	`sex`	TEXT NOT NULL
);

CREATE TABLE `poll` (
	`poll_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`city`	TEXT NOT NULL,
	`emotion`	TEXT NOT NULL,
	`month`	TEXT NOT NULL,
	`poll_time`	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author_id`	INTEGER,   
  FOREIGN KEY(`author_id`) REFERENCES `author`(id) ON DELETE CASCADE ON UPDATE CASCADE
);

