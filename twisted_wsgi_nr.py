#!/usr/bin/env python

import newrelic.agent
newrelic.agent.initialize()

import logging
import json
import os
import sys

import falcon
import structlog

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site, Request
from twisted.internet import reactor
from twisted.python import log as twLog
# from twisted.logger import (
#     Logger, FileLogObserver, globalLogPublisher,
#     jsonFileLogObserver
# )
logger = structlog.getLogger()


class QuoteResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': 'I\'ve always been more interested in the future than in the past.',
            'author': 'Grace Hopper'
        }
        # this is a structlog logger
        log = logger.new(whom=quote["author"], what=quote["quote"])
        log.msg("quoted!")
        resp.body = json.dumps(quote)


def run():
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
    # grab all of the events that are dispatched to stdlib logger
    # new relic uses this.
    handler = logging.StreamHandler(sys.stdout)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

    # start the twisted logger
    twLog.startLogging(sys.stdout)
    # api is the WSGI resource returned by Falcon.
    api = falcon.API()
    api.add_route('/quote', QuoteResource())

    app = newrelic.agent.WSGIApplicationWrapper(api)
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)

    reactor.listenTCP(port=8713, factory=site)
    reactor.run()


if __name__ == '__main__':
    run()
