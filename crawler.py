""" Crawler module.

This module responsible for gathering words from a web resources,
preparing them(cutting html tags, scrips and so on), skip prepositions
and articles, stores data to db and so on.
"""
import os
import re

from bs4 import BeautifulSoup

from collections import Counter, OrderedDict

import db
import utils


EXCEPTIONS = ['AN', 'THE', 'IN', 'ON', 'AT', 'WITH', 'TO', 'FROM', 'AND',
              'FOR', 'OF', 'BY', 'IS', 'AS', 'ARE', 'HOW', 'WHAT', 'THAT',
              'AFTER', 'BEFORE', 'YOU', 'HE', 'WE', 'OFF', 'BE', 'THIS']
PEM_KEY_LOCATION = '/home/psavyuk/myapp/ChallengeTestWords/key.pem'

import MySQLdb
# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            db='wordschallenge',
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)
    else:
        db = MySQLdb.connect(host='127.0.0.1',
                             db='wordschallenge',
                             user=CLOUDSQL_USER,
                             passwd=CLOUDSQL_PASSWORD)

    return db

class Crawler(object):
    """ Crawler class. """

    def __init__(self, url):
        """ Docstring on the __init__ method.

        param: url Resource URL
        """
        self.url = url
        self.html = self.get_raw_site_content()
        self.text = self.get_content_without_tags()
        self.counters = self.get_words_couners()
        self.updates_db_data()

    def get_raw_site_content(self):
        """ Gets raw site content with html tags and so on.

        return decoded to UTF-8 content data.
        """
        try:
            from urllib.request import urlopen
        except ImportError:
            from urllib2 import urlopen
        response = urlopen(self.url)
        data = response.read()
        return data.decode('utf-8')

    def get_content_without_tags(self):
        """ Creans raw data to the text.

        return clear text.
        """
        soup = BeautifulSoup(self.html, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)

    def get_words_couners(self):
        """ Counts words.

        return OrderedDict with top 100 frequency used words.
        """
        words_dict = {}
        words = re.findall(r'[\w^\d]{2,}', self.text, flags=re.U)
        cap_words = [word.upper() for word in words]

        word_counts = Counter(cap_words)
        for key, value in word_counts.items():
            if key not in EXCEPTIONS and not key.isdigit():
                words_dict[key] = value
        return OrderedDict(sorted(words_dict.items(),
                                  key=lambda x: x[1],
                                  reverse=True)[:100])

    def updates_db_data(self):
        """ Updates db with new data. """
        #dbconn = connect_to_cloudsql()
        lst = list((self.counters).items())
        for word, counter in lst:
            try:
                word_hash = utils.get_word_hash(word)
                word_encrypted = \
                    utils.encrypt_RSA(PEM_KEY_LOCATION,
                                      word)
                #db.manage_data(dbconn, word_hash, word_encrypted, counter)
            except ValueError as err:
                print(err)
                continue


class Admin(object):
    """ Admin class. """

    def __init__(self):
        """ Docstring on the __init__ method. """
        #dbconn = connect_to_cloudsql()
        self.data = db.get_admin_data(dbconn)

    def get_data(self):
        """ Returns all words from the db. """
        words_and_counters = {}
        for word, counter in self.data:
            word = utils.decrypt_RSA(PEM_KEY_LOCATION,
                                     word)
            words_and_counters[word] = counter
        return OrderedDict(sorted(words_and_counters.items(),
                                  key=lambda x: x[1],
                                  reverse=True))
