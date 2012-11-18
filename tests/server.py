#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))


from simpleurl import SimpleURL
from brubeck.request_handling import Brubeck, render
from brubeck.connections import WSGIConnection

brubeck_app = Brubeck(msg_conn=WSGIConnection())
app = SimpleURL(brubeck_app)

body_success = u'Success'


def index(application, message):
    return render(body_success, 200, 'OK', {})


def one(application, message):
    return render(body_success, 200, 'OK', {})


@app.add_route('/all/', defaults={'ids': 1}, method=['GET', 'POST'])
@app.add_route('/all/<ids>', method=['GET', 'POST'])
def process(application, message, ids):
    return render(body_success, 200, 'OK', {})


@app.add_route('/float/<float:value>')
def check_float(application, message, value):
    return render(body_success, 200, 'OK', {})


# Note: its is method is methods, since brubeck uses method.
@app.add_route('/int/<int:value>', endpoint='check_int', method=['GET'])
def check_int(application, message, value):
    return render(body_success, 200, 'OK', {})

app.add_route_url('/', 'index', index)
app.add_route_url('/one', 'one', one)

if __name__ == "__main__":
    app.run()
