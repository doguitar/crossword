#!/usr/bin/env python

import cherrypy
import os
import time
import manager
import json
import datetime

from mako.lookup import TemplateLookup


class Host(object):
    url_base = "/"
    base_path = None
    cache_string = 'max-age=432000'
    stopping = False
    manager = None

    def get_username(self):
        return cherrypy.request.cookie['username'].value if 'username' in cherrypy.request.cookie.keys() else None

    def __init__(self, base_path, url_base):
        self.base_path = base_path
        self.url_base = url_base
        self.lookup = TemplateLookup(directories=[os.path.join(self.base_path, "html", "templates")])
        self.manager = manager.Manager(base_path, os.path.join(base_path, "host.db"))

    def __get_template(self, template):
        return self.lookup.get_template(template)

    @cherrypy.expose
    def index(self):
        return self.__get_template("index.mako").render(
                base=self.url_base,
                crosswords=self.manager.database.select_puzzles(),
                username=self.get_username())

    @cherrypy.expose
    def login(self, username):
        user = self.manager.database.select_user(username)
        if not user:
            self.manager.database.insert_user(username)

        cherrypy.response.cookie['username'] = username
        cherrypy.response.cookie['username']['max-age'] = 43200
        cherrypy.response.cookie['username']['path'] = self.url_base
        raise cherrypy.HTTPRedirect(self.url_base)

    @cherrypy.expose
    def crossword(self, puzzle_id, session_id=None):
        user = self.get_username()
        if not user:
            raise cherrypy.HTTPRedirect(self.url_base)

        if not session_id:
            session_id = self.manager.database.insert_session(int(puzzle_id))
            raise cherrypy.HTTPRedirect(self.url_base + '/'.join(["crossword", str(puzzle_id), str(session_id)]))


        puzzle = json.loads(self.manager.database.select_puzzle(int(puzzle_id))["JSON"])
        return self.__get_template("crossword.mako").render(
                base=self.url_base,
                puzzle=puzzle,
                clues=json.dumps(puzzle["clues"]))

    @cherrypy.expose
    def sql(self, sql=None):
        start = time.clock()
        rows = self.manager.database.execute_sql(sql) if sql else None
        elapsed = (time.clock() - start)

        return self.__get_template("sql.mako").render(
                base=self.url_base,
                elapsed=elapsed,
                rows=rows,
                sql=sql)

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
        result = None
        if type == "move":
            x = int(kwargs['cord_x'])
            y = int(kwargs['cord_y'])
            char = kwargs['char']
            session_id = kwargs['session_id']
            self.manager.database.insert_move(session_id, self.get_username(), x, y, char, datetime.datetime.utcnow())

        elif type == "moves":
            session_id = kwargs['session_id']
            since = kwargs['since']
            moves = self.manager.database.select_move(session_id, self.get_username(), int(since))

            result = json.dumps(moves)
        return result

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
