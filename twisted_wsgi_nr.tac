import newrelic.agent
newrelic.agent.initialize()

import falcon
import json
import os
import sys

import logging
import structlog

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site, Request
from twisted.internet import reactor
from twisted.application.service import Application

from twisted.application.internet import (
    TCPServer,
    SSLServer
)


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


#def run():
# api is the WSGI resource returned by Falcon.
structlog.configure(
    processors=[
        structlog.processors.StackInfoRenderer(),
        structlog.twisted.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.twisted.LoggerFactory(),
    wrapper_class=structlog.twisted.BoundLogger,
    cache_logger_on_first_use=True,
)

# setup the root loggers
handler = logging.StreamHandler(sys.stdout)
root_logger = logging.getLogger()
root_logger.addHandler(handler)


wsgi_app = falcon.API()
wsgi_app.add_route('/quote', QuoteResource())

app = newrelic.agent.WSGIApplicationWrapper(wsgi_app)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
site.displayTracebacks = False

application = Application("twisted-wsgi-newrelic-test")
wsgi_service = TCPServer(8713, site)
wsgi_service.setServiceParent(application)
