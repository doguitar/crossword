#!/usr/bin/env python

import datetime
import cherrypy
import os
import re
import urllib
import sys
import shutil
import threading
import time
import copy
import json
from cherrypy.lib.static import serve_file
from mako.template import Template
from mako.lookup import TemplateLookup
from multiprocessing import Process


class Host(object):
    _url_base = "/"
    _base_path = None
    _cache_string = 'max-age=432000'
    _stopping = False

    def __init__(self, base_path, url_base):
        self._base_path = base_path
        self._url_base = url_base
        self._lookup = TemplateLookup(directories=[os.path.join(self._base_path, "html", "templates")])

    def __get_template(self, template):
        return self._lookup.get_template(template)

    @cherrypy.expose
    def index(self):
        return self.__get_template("index.mako").render(base=self._url_base)

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def js(self, path=None):
        cherrypy.response.headers['Content-Type'] = 'text/javascript'
        cherrypy.response.headers['Cache-Control'] = self._cache_string
        return open(os.path.join(self._base_path, path))

    @cherrypy.expose
    def json(self, type, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def css(self, path=None):
        cherrypy.response.headers['Content-Type'] = 'text/css'
        cherrypy.response.headers['Cache-Control'] = self._cache_string
        return open(os.path.join(self._base_path, path))

try:
    print "launching"

    app_config = {
        '/': {
            'tools.auth_basic.on': False,
            'tools.gzip.on': True,
            'tools.gzip.mime_types': ['text/*', 'image/*', 'application/*']
        }
    }

    cherrypy.config.update(
        {
              'server.socket_host': '0.0.0.0'
            , 'server.socket_port': 4567
            , 'thread_pool': 100
        })
    current_directory = os.path.dirname(os.path.realpath(__file__))
    cherrypy.tree.mount(
        Host(current_directory, "/"), config=app_config)
    cherrypy.engine.start()
    print "launched"
    cherrypy.engine.block()
except Exception as e:
    print e
