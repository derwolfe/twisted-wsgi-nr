import newrelic.agent
newrelic.agent.initialize()

import falcon
import json
import os

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site, Request
from twisted.internet import reactor


from twisted.logger import Logger
log = Logger()


class QuoteResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        log.warn('quoted', whom='me')
        quote = {
            'quote': 'I\'ve always been more interested in the future than in the past.',
            'author': 'Grace Hopper'
        }

        resp.body = json.dumps(quote)


def run():
    # api is the WSGI resource returned by Falcon.
    api = falcon.API()
    api.add_route('/quote', QuoteResource())

    app = newrelic.agent.WSGIApplicationWrapper(api)
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(port=8713, factory=site)
    reactor.run()
