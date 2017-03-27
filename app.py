"""Tornado Webserver staff.

This module based on Tornado whicn is a Python web framework
and asynchronous networking library.
"""

import os
import tornado.ioloop
import tornado.web

import utils

from crawler import Admin, Crawler


# This tells tornado where to find the template files
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    debug=True
)


class IndexPageHandler(tornado.web.RequestHandler):
    """ Class responsible for handle index page requests. """

    def get(self):
        """ Refelects index page. """
        self.render("index.html")

    def post(self):
        """ Returns wrapped to html json top100 words data. """
        uri = self.get_argument('url')
        if utils.uri_validator(uri) and uri:
            words = Crawler(uri).counters
            self.render("top100.html", items=words)
        else:
            self.write('Wrong url format. \
                       Tips: Should start from schema http(s)://abc.abc')


class AdminHandler(tornado.web.RequestHandler):
    """ Class responsible for handle admin page requests. """

    def get(self):
        """ Returns wrapped to html json all words data. """
        words_and_counters = Admin().get_data()
        self.render("admin.html", items=words_and_counters)


def make_app():
    """ Make app func. """
    return tornado.web.Application([
        (r"/", IndexPageHandler),
        (r"/admin", AdminHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
