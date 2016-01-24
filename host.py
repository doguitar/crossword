#!/usr/bin/env python

import cherrypy
import os
import time
import manager
import json

from mako.lookup import TemplateLookup


class Host(object):
    url_base = "/"
    base_path = None
    cache_string = 'max-age=432000'
    stopping = False
    manager = None

    def __init__(self, base_path, url_base):
        self.base_path = base_path
        self.url_base = url_base
        self.lookup = TemplateLookup(directories=[os.path.join(self.base_path, "html", "templates")])
        self.manager = manager.Manager(base_path, os.path.join(base_path, "host.db"))

    def __get_template(self, template):
        return self.lookup.get_template(template)

    @cherrypy.expose
    def index(self):
        puzzle = self.manager.read_puzzle(os.path.join(self.base_path, "crosswords", "2016-1-16-LosAngelesTimes.puz"))
        return self.__get_template("index.mako").render(base=self.url_base, puzzle=puzzle, clues=json.dumps(puzzle["clues"]))

    @cherrypy.expose
    def sql(self, sql=None):
        start = time.clock()
        rows = self.manager.database.execute_sql(sql) if sql else None
        elapsed = (time.clock() - start)

        return self.__get_template("sql.mako").render(base=self.url_base, elapsed=elapsed, rows=rows)

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def js(self, path=None):
        cherrypy.response.headers['Content-Type'] = 'text/javascript'
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return open(os.path.join(self.base_path, "html", "js", path))

    @cherrypy.expose
    def json(self, type, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def css(self, path=None):
        cherrypy.response.headers['Content-Type'] = 'text/css'
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return open(os.path.join(self.base_path, "html", "css", path))

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
