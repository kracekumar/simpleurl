#!/usr/bin/env python


from brubeck.request_handling import Brubeck, WebMessageHandler, render
from brubeck.connections import WSGIConnection
from simpleurl import SimpleURL


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
        ('/fun/<name>', name_handler),
        ('/', IndexHandler)]

config = {
    'msg_conn': WSGIConnection(),
    'handler_tuples': urls,
}

brubeck_app = Brubeck(**config)
app = SimpleURL(brubeck_app)


@app.add_route('/deco/<name>', method='GET')
def new_name_handler(application, message, name):
    return render('Take five, %s!' % (name), 200, 'OK', {})


app.run()
