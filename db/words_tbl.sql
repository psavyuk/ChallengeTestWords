CREATE TABLE words_tbl(
        word_hash CHAR(128) NOT NULL,
	word_encrypted TEXT NOT NULL,
	word_frequency INT NOT NULL,
   PRIMARY KEY ( word_hash )
);
