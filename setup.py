#! -*- coding :utf-8 -*-

"""
SimpleURL
======

SimpleURL is based on Werkzeug routing system for Brubeck.

Why not use regex based routing system?
----

- Regex is hard.

- Too complicated.

- Easy to make mistake.
    Example
    ----
    @app.add_url_route('^/brubeck')
    @app.add_url_route('^/brubeck/\d')

    Above regex routes seems to be different but not.
    Request - `/brubeck` and `/brubeck/1` will match first because
    you have failed to place `$` at the end. As a developer you are not supposed
    to waste your time writing clever regex and debugging regex.


Why Werkzeug ?
----

- Simple

- Extensively documented

- Active community

- Fully WSGI compatible

- Various utility functions for dealing with HTTP headers such as
    `Accept` and `Cache-Control` headers


Development
---

The SimpleURL development version can be installed by cloning the git
repository from `github`_::

    git clone git@github.com:kracekumar/simpleurl.git

.. _github: http://github.com/kracekumar/simpleurl
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from simpleurl import version

setup(
    name='SimpleURL',
    version=version,
    url='https://github.com/kracekumar/simpleurl',
    license='Lesser General Public License (LGPL)',
    author='kracekumar',
    author_email='me@kracekumar.com',
    description='Werkzeug based routing system for Brubeck - Escape from Regex',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['simpleurl'],
    include_package_data=True,
    zip_safe=False,
    platforms='any'
)
