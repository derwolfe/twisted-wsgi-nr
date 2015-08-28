import newrelic.agent
newrelic.agent.initialize()

import falcon
import json
import os

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site, Request
from twisted.internet import reactor

from structlog import get_logger, configure, twisted
from structlog.stdlib import LoggerFactory

configure(
   processors=[twisted.JSONRenderer()],
   context_class=dict,
   logger_factory=twisted.LoggerFactory(),
   wrapper_class=twisted.BoundLogger,
   cache_logger_on_first_use=True,
)

log = get_logger()


class QuoteResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        log.info('quoted', whom='me')
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
