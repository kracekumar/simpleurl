SimpleURL
=========

   :image:: https://secure.travis-ci.org/kracekumar/simpleurl.png?branch=master
   :target: http://travis-ci.org/kracekumar/simpleurl

SimpleURL is based on Werkzeug routing system for Brubeck.

Why not use regex based routing system?
---------------------------------------

- Regex is hard.

- Too complicated.

- Easy to make mistake.

    - Example

    ```
    @app.add_url_route('^/brubeck')
    @app.add_url_route('^/brubeck/\d')
    ```

    Above regex routes seems to be different but not.
    Request - `/brubeck` and `/brubeck/1` will match first because
    you have failed to place `$` at the end. As a developer you are not supposed
    to waste your time writing clever regex and debugging regex.


Why Werkzeug ?
--------------

- Simple

- Extensively documented

- Active community

- Fully WSGI compatible

- Various utility functions for dealing with HTTP headers such as
    `Accept` and `Cache-Control` headers


Talk is cheap, show me the code
-------------------------------

```
#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from simpleurl import SimpleURL
from brubeck.request_handling import Brubeck, render
from brubeck.connections import Mongrel2Connection

brubeck_app = Brubeck(msg_conn=Mongrel2Connection('tcp://127.0.0.1:9999',
                                          'tcp://127.0.0.1:9998'))
app = SimpleURL(brubeck_app)


def index(application, message):
    body = 'Take five index'
    return render(body, 200, 'OK', {})


def one(application, message):
    body = 'Take five one'
    return render(body, 200, 'OK', {})

#: Default value
@app.add_route('/all/', defaults={'ids': 1}, method=['GET', 'POST'])
@app.add_route('/all/<ids>', method=['GET', 'POST'])
def process(application, message, ids):
    body = 'Take five - %s times' % (str(ids))
    return render(body, 200, 'OK', {})

#: float value for urls
@app.add_route('/float/<float:value>')
def check_float(application, message, value):
    return render("You passed float value:%s" % str(value), 200, 'OK', {})


# Note: its is method is methods, since brubeck uses method.
@app.add_route('/int/<int:value>', endpoint='check_int', method=['GET'])
def check_int(application, message, value):
    return render("You passed int:%s" % str(value), 200, 'OK', {})

app.add_route_url('/', 'index', index)
app.add_route_url('/one', 'one', one)
app.run()

# If URL Rule is not found `werkzeug.exceptions.NotFound: 404: Not Found` is raised
```

Note:
-----
From Flask quick start page

Unique URLs / Redirection Behavior
------
The idea behind that module is to ensure beautiful and unique URLs based on precedents laid down by Apache and earlier HTTP servers.

Take these two rules:

```
@app.add_route('/projects/')
def projects():
    return render('The project page', 200, 'OK', {})

@app.add_route('/about')
def about():
    return render('The about page', 200, 'OK', {})
```

Though they look rather similar, they differ in their use of the trailing slash in the URL definition. In the first case, the canonical URL for the projects endpoint has a trailing slash. In that sense, it is similar to a folder on a file system. Accessing it without a trailing slash will cause Flask to redirect to the canonical URL with the trailing slash.

In the second case, however, the URL is defined without a trailing slash, rather like the pathname of a file on UNIX-like systems. Accessing the URL with a trailing slash will produce a 404 “Not Found” error.

This behavior allows relative URLs to continue working if users access the page when they forget a trailing slash, consistent with how Apache and other servers work. Also, the URLs will stay unique, which helps search engines avoid indexing the same page twice.

Reference
---------

For more info about [Werkzeug Routing](http://werkzeug.pocoo.org/docs/routing/)


Development
-----------

The SimpleURL development version can be installed by cloning the git
repository from [github](http://github.com/kracekumar/simpleurl)

    `git clone git@github.com:kracekumar/simpleurl.git`


