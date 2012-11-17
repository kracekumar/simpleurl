#! -*- coding: utf-8 -*-

# Most of the code here is inspired from
# https://github.com/mitsuhiko/flask/blob/master/flask/app.py

version = "0.0.2"
version_info = (0, 0, 2)

import inspect

from brubeck.request_handling import Brubeck
from werkzeug.routing import Rule, Map


# Helpers
def _return_func_name(view_func):
    # helper to return func name for the url
    assert view_func is not None, 'expected view func if endpoint '
    return view_func.__name__


class SimpleURL(Brubeck):
    """SimpleURL is alternate to Brubeck Regex based routing.
    SimpleURL uses werkzeug routing to make routing simpler.
    """
    def __init__(self, brubeck_object):
        super(Brubeck, self).__init__()
        # copy all brubeck object attributes to simpleurl.
        for key, val in brubeck_object.__dict__.iteritems():
            setattr(self, key, val)
        #: Werkzeug Rule class
        self.url_rule_class = Rule
        #: Map object which stores all the Rules
        self.url_map = Map()
        #: A dictionary of all view functions registered.  The keys will
        #: be function names which are also used to generate URLs and
        #: the values are the function objects themselves.
        #: To register a view function, use the :meth:`route` decorator.
        self.view_functions = {}

    def add_route_url(self, rule, endpoint=None, view_func=None, **options):
        """Registration point for all URL rules.
        Basically this example::

            @app.add_route('/')
            def index(application, message):
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_route_rule('/', 'index', index)

        If the view_func is not provided you will need to connect the endpoint
        to a view function like so::

            app.view_functions['index'] = index

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param view_func: the function to call when serving a request to the
                          provided endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (`GET`, `POST` etc.).  By default a rule
                        just listens for `GET` (and implicitly `HEAD`).
        """
        if endpoint is None:
            endpoint = _return_func_name(view_func)
        options['endpoint'] = endpoint
        method = options.pop('method', None)

        if method is None:
            method = getattr(view_func, 'method', None) or ('GET',)
        method = set(method)

        # Methods that should always be added
        required_method = set(getattr(view_func, 'required_methods', ()))

        # Add the required methods now.
        method |= required_method

        # due to a werkzeug bug we need to make sure that the defaults are
        # None if they are an empty dictionary.  This should not be necessary
        # with Werkzeug 0.7
        options['defaults'] = options.get('defaults') or None

        rule = self.url_rule_class(rule, methods=method, **options)
        #rule.provide_automatic_options = provide_automatic_options

        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func is not view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func

    def add_route(self, rule, method=['GET'], **options):
        """A decorator that is used to register a view function for a
        given URL rule.  This does the same thing as :meth:`add_url_rule`
        but is intended for decorator usage::

            @app.add_route('/', method=['GET', 'POST'])
            def index(application, message):
                if message.method == 'GET':
                    # import render from brubeck.request_handling
                    return render("Foo Bar", 200, 'OK', {})
                    return render('Hello World'
                elif message.method == 'POST':
                    # process the arguments
                    # return render

            # Passing default values
            @app.add_route('/all/', defaults={'ids': 1}, method=['GET', 'POST'])
            @app.add_route('/all/<ids>', method=['GET', 'POST'])
            def process(application, message, ids):
                body = 'you passed id as %s' % (str(ids))
                return render(body, 200, 'OK', {})


        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param view_func: the function to call when serving a request to the
                          provided endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (`GET`, `POST` etc.).
        """
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_route_url(rule, endpoint, f, **options)
            return f
        return decorator

    def route_message(self, message):
        self.url_rule_class.add = self.url_map
        # FIX ME: Figure out different values of url_scheme
        # FIX ME: Convert brubeck message to WSGI Request so that it is easy to use bind_to_environ
        # print type(message)
        headers = message.headers
        arguments = message.arguments or None
        url_path = message.path
        self.urls = self.url_map.bind(server_name=headers[u'host'], url_scheme=headers[u'VERSION'].split('/')[0],
             default_method=message.method, path_info=url_path, query_args=arguments)
        endpoint = self.urls.match(message.path)
        kallable = self.view_functions[endpoint[0]]
        if inspect.isclass(kallable):
            raise NotImplementedError("SimpleURL doesn't support class based Routing yet :-(. Work in Progres")
        else:
            handler = lambda: kallable(self, message, **endpoint[1])
            return handler
