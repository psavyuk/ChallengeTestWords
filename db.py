""" DB module staff.

This module responsible for collaborations between app and db.
"""

import os
import utils


def dbwrap(func):
    """Wrap a function in an idomatic SQL transaction. The wrapped function
    should take a cursor as its first argument; other arguments will be
    preserved.
    """
    def new_func(conn, *args, **kwargs):
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN")
            ret = func(cursor, *args, **kwargs)
            cursor.execute("COMMIT")
        except:
            cursor.execute("ROLLBACK")
            raise
        finally:
            cursor.close()

        return ret

    return new_func


@dbwrap
def get_all_words_hashes(cursor):
    """ Returns all words hashes from the words_tbl table. """
    cursor.execute("SELECT word_hash FROM words_tbl;")
    return cursor.fetchall()


@dbwrap
def get_all_words_and_counters(cursor):
    """ Returns all words words and counters from the words_tbl table. """
    cursor.execute("SELECT word_encrypted, word_frequency FROM words_tbl;")
    return cursor.fetchall()


@dbwrap
def add_word(cursor, word_hash, word_encrypted, word_frequency):
    """ Adds single records(word_hash, word_encrypted, word_frequency)
    to the words_tbl.
    """
    query = """ INSERT INTO words_tbl (word_hash, word_encrypted,
                word_frequency) VALUES (%s, %s, %s) """
    cursor.execute(query, (word_hash, word_encrypted, word_frequency))


@dbwrap
def update_word(cursor, word_frequency, word_hash):
    """ Updates single record(word_encrypted, word_frequency)
    to the words_tbl.
    """
    query = """ UPDATE words_tbl
                SET word_frequency = %s
                WHERE word_hash = %s """
    cursor.execute(query, (word_frequency, word_hash))


def manage_data(dbconn, word_hash, word_encrypted, word_frequency):
    """ Manages inserting and updating process.

    param: word_hash(str) Word salted hash
    param: word_encrypted(str) RSA encrypted word
    param: word_frequency(int) Word frequency in the text
    """
    words_hashes = get_all_words_hashes(DBCONN)
 
    words_hashes_list = [element for tupl in words_hashes for element in tupl]
    if word_hash in words_hashes_list:
        update_word(dbconn, word_frequency, word_hash)
    else:
        add_word(dbconn, word_hash, word_encrypted, word_frequency)


def get_admin_data(dbconn):
    """ Returns all data for admin page. """
    return get_all_words_and_counters(dbconn)
