CREATE TABLE survey (
  id INTEGER NOT NULL PRIMARY KEY,
  remote_addr VARCHAR(250),
  timestamp DATETIME,
  natres_pubtrans REAL NOT NULL,
  natres_habitat REAL NOT NULL,
  natres_housing REAL NOT NULL
);
