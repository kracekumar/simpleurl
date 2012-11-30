#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import unittest
import requests


GET_URLS = {200: ['/', '/all/', '/all/2', '/float/3.14', '/int/3',
                '/class/class', '/deco/decorator', '/fun/fun'],
    404: ['/foo', '/all']}

POST_URLS = {200: [
                    {'url': '/class/class', 'data': {'framework': 'brubeck'}},
                ],
            }

from time import sleep
sleep(5)

import os
print(os.system("ps aux"))

class TestNoClassesSimpleURL(unittest.TestCase):
    def testGetURL(self):
        for key, val in GET_URLS.iteritems():
            for url in val:
                self.assertEqual(\
                    requests.get("http://localhost:6767%s" % (url)).status_code,\
                     key)

    def testPostURL(self):
        for key, val in POST_URLS.iteritems():
            for item in val:
                self.assertEqual(\
                    requests.post("http://localhost:6767%s" % (item['url']), data=item['data']).status_code,\
                     key)


if __name__ == '__main__':
    unittest.main()
