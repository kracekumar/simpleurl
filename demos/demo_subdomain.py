#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from simpleurl import SimpleURL
from brubeck.request_handling import Brubeck, render
from brubeck.connections import Mongrel2Connection

#brubeck_app = Brubeck(msg_conn=WSGIConnection())
brubeck_app = Brubeck(msg_conn=Mongrel2Connection('tcp://127.0.0.1:9999',
                                          'tcp://127.0.0.1:9998'))
app = SimpleURL(brubeck_app)


def index(application, message):
    body = 'Take five index'
    return render(body, 200, 'OK', {})


def one(application, message):
    body = 'Take five one'
    return render(body, 200, 'OK', {})


@app.add_route('/all/', defaults={'ids': 1}, method=['GET', 'POST'])
@app.add_route('/all/<ids>', method=['GET', 'POST'])
def process(application, message, ids):
    body = 'Take five - %s' % (str(ids))
    return render(body, 200, 'OK', {})


@app.add_route('/float/<float:value>')
def check_float(application, message, value):
    return render("You passed float value:%s" % str(value), 200, 'OK', {})


# Note: its is method is methods, since brubeck uses method.
@app.add_route('/int/<int:value>', endpoint='check_int', subdomain='brubeck', method=['GET'])
def check_int(application, message, value):
    return render("You passed int:%s" % str(value), 200, 'OK', {})

app.add_route_url('/', 'index', index)
app.add_route_url('/one', 'one', one, subdomain='brubeck')
app.run()
