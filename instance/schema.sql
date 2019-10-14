DROP TABLE IF EXISTS pages;
DROP TABLE IF EXISTS user;

CREATE TABLE pages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  order_number INTEGER NULL,
  page_title TEXT NOT NULL,
  page_url TEXT NOT NULL,
  page_domain TEXT NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);