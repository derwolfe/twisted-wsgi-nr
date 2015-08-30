import newrelic.agent
newrelic.agent.initialize()

import falcon
import json
import os
import sys

import structlog

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site, Request
from twisted.internet import reactor
from twisted.python.log import startLogging


logger = structlog.getLogger()


class QuoteResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'I\'ve always been more interested in the future than in the past.',
            'author': 'Grace Hopper'
        }
        log = logger.new(whom=quote["author"], what=quote["quote"])
        log.msg("quoted!")
        resp.body = json.dumps(quote)


def run():
    # api is the WSGI resource returned by Falcon.
    startLogging(sys.stdout)
    structlog.configure(
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.twisted.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.twisted.LoggerFactory(),
        wrapper_class=structlog.twisted.BoundLogger,
        cache_logger_on_first_use=True,
    )

    api = falcon.API()
    api.add_route('/quote', QuoteResource())

    app = newrelic.agent.WSGIApplicationWrapper(api)
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(port=8713, factory=site)
    reactor.run()

if __name__ == '__main__':
    run()
