#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))


from simpleurl import SimpleURL
from brubeck.connections import WSGIConnection
from brubeck.request_handling import Brubeck, WebMessageHandler, render


class IndexHandler(WebMessageHandler):
    def get(self):
        self.set_body('Take five!')
        return self.render()


class NameHandler(WebMessageHandler):
    def get(self, name):
        self.set_body('Take five, %s!' % (name))
        return self.render()

    def post(self, name):
        self.set_body('Take five post, {0} \n POST params: {1}\n'.format(name, self.message.arguments))
        return self.render()


def name_handler(application, message, name):
    return render('Take five, %s!' % (name), 200, 'OK', {})


urls = [('/class/<name>', NameHandler),
        ('/fun/<name>', name_handler)
        ]

config = {
    'msg_conn': WSGIConnection(),
    'handler_tuples': urls,
}

brubeck_app = Brubeck(**config)
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


@app.add_route('/deco/<name>', method='GET')
def new_name_handler(application, message, name):
    return render('Take five, %s!' % (name), 200, 'OK', {})


if __name__ == "__main__":
    print("Run here")
    app.run()
