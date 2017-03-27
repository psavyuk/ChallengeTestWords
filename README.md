Frequency words app

    This application bases on Tornado Web Server. 
Modules:
- crawler - main worker performs all work related with grubbing and preparint data.
- db - performs db operation like READ, INSERT, UPDATE
- utils - useful functions(encrypt_RSA, decrypt_RSA, generate_salt_hash) 
- generate_pem - generates a pem key
- app - Tornado Web Server

Main workflow:
When you go to localhost(IP, host):8888/ You will get a chance to insert a data(URL) in appropriate format like(http(s)://abc.abc) otherwise You will get a message that your URL is an incorrect. When you entered correct URL, browser will send post request to the server withit. Backend part(crawler) will get this URL and read all raw data from it, after that using beautiful soup module deletes all useless for crawler data like scripts,
css and html tags and counts all words. Returns wrapped data to the UI and stores into DataBase. On UI You will get table with the most frequently used words and counters sorting by DESC.

Stored data to the DataBase:
1. Created words_tbl table:
mysql> desc words_tbl;
+----------------+-----------+------+-----+---------+-------+
| Field          | Type      | Null | Key | Default | Extra |
+----------------+-----------+------+-----+---------+-------+
| word_hash      | char(128) | NO   | PRI | NULL    |       |
| word_encrypted | text      | NO   |     | NULL    |       |
| word_frequency | int(11)   | NO   |     | NULL    |       |
+----------------+-----------+------+-----+---------+-------+
3 rows in set (0.16 sec)

word_hash will contain salted word hash(The primary key for the word is a salted hash of the word.)
word_encrypted will contain RSA encrypted word(UTF-8)(The word itself is saved in a column that has asymmetrical encryption, and you are saving the encrypted version of the word.)
word_frequency will contain integer value - counter(The total frequency count of the word).

Crawler can perform only READ, CREATE, UPDATE operations. Notice: DELETE is strongly PROHIBITED.

When you go to localhost(IP, host):8888/admin page.
The “admin” page, that will list all words entered into the DB, ordered by frequency of usage, visible in decrypted form.
