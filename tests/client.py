#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import unittest
import requests


URLS = {200: ['/', '/all/', '/all/2', '/float/3.14', '/int/3'],
    404: ['/foo', '/all']}

from time import sleep
sleep(5)


class TestNoClassesSimpleURL(unittest.TestCase):
    def testURL(self):
        for key, val in URLS.iteritems():
            for url in val:
                self.assertEqual(\
                    requests.get("http://localhost:6767%s" % (url)).status_code,\
                     key)

if __name__ == '__main__':
    unittest.main()
