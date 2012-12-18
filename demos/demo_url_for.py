#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from simpleurl import SimpleURL
from brubeck.request_handling import Brubeck, render
from brubeck.connections import WSGIConnection

brubeck_app = Brubeck(msg_conn=WSGIConnection())
app = SimpleURL(brubeck_app)


@app.add_route("/index")
def index(application, message):
    return render("index", 200, 'OK', {})


@app.add_route('/', defaults={'a': 3})
@app.add_route("/<int:a>")
def handle_int(application, message, a):
        return render("You passed int value:%s" % str(a), 200, 'OK', {})


@app.add_route('/test_endpoint', endpoint='test_endpoint')
def test(application, message):
    return render("Test Endpoint", 200, 'OK', {})


@app.add_route('/test')
def test(application, message):
    u_index = app.url_for('index')
    u_handle_int = app.url_for('handle_int', a=23)
    d_handle_int = app.url_for('handle_int', method='POST')
    u_test_endpoint = app.url_for('test_endpoint', external=True)
    return render("url_for output: index: %s, handle_int: %s, default_param: %s, test_endpoint: %s" %(u_index, 
        u_handle_int, d_handle_int, u_test_endpoint), 200, 'OK', {})

app.run()
