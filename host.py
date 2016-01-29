#!/usr/bin/env python

import cherrypy
import os
import time
import manager
import json
import datetime

from mako.lookup import TemplateLookup
from cherrypy.lib.static import serve_file


class Host(object):
    url_base = "/"
    base_path = None
    cache_string = 'max-age=432000'
    manager = None

    def __init__(self, base_path, url_base):
        self.base_path = base_path
        self.url_base = url_base
        self.lookup = TemplateLookup(directories=[os.path.join(self.base_path, "html", "templates")])
        self.manager = manager.Manager(base_path, os.path.join(base_path, "host.db"))
        cherrypy.engine.subscribe('stop', self.__del__())

    def __del__(self):
        self.manager.__del__()

    def save_cookie(self, name, value):
        cherrypy.response.cookie[name] = value
        cherrypy.response.cookie[name]['max-age'] = 43200
        cherrypy.response.cookie[name]['path'] = self.url_base

    def get_hash(self):
        user_hash = cherrypy.request.cookie['hash'].value if 'hash' in cherrypy.request.cookie.keys() else None
        return user_hash

    def valid_hash(self):
        user_hash = self.get_hash()
        if user_hash:
            user_hash = self.manager.database.select_user(user_hash)
            if not user_hash:
                self.save_cookie('hash', '')
            else:
                user_hash = user_hash['Hash']
        return user_hash

    def __get_template(self, template):
        return self.lookup.get_template(template)

    @cherrypy.expose
    def index(self, r=''):
        return self.__get_template("index.mako").render(
                base=self.url_base,
                crosswords=sorted(self.manager.database.select_puzzles(), key=lambda p: p["Timestamp"], reverse=True),
                username=self.get_hash(),
                return_url=r)

    @cherrypy.expose
    def login(self, display=None, email=None, password=None, confirm=None, r=None):
        if email and not (display or password or confirm):
            return "exists" if self.manager.database.select_user_by_email(email) else ""

        if email and password:
            if confirm and confirm == password:
                self.manager.database.insert_user(display, email, password)

            userhash = self.manager.database.login(email, password)
            if userhash:
                self.save_cookie('hash', userhash)

        redirect = r or '/'
        raise cherrypy.HTTPRedirect(redirect)

    @cherrypy.expose
    def crossword(self, puzzle_id, session_id=None):
        if puzzle_id.isdigit():
            puzzle_id = int(puzzle_id)
        else:
            raise cherrypy.HTTPRedirect('')
        if session_id and session_id.isdigit():
            session_id = int(session_id)

        user_hash = self.valid_hash()
        if not user_hash:
            if session_id:
                raise cherrypy.HTTPRedirect("/?r=/crossword/{0}/{1}".format(puzzle_id, session_id))
            else:
                raise cherrypy.HTTPRedirect("/?r=/crossword/{0}".format(puzzle_id))

        if not session_id:
            session_id = self.manager.database.get_user_session(puzzle_id, user_hash)
            if not session_id:
                session_id = self.manager.database.insert_session(puzzle_id, user_hash)
            raise cherrypy.HTTPRedirect('/'.join(["/crossword", str(puzzle_id), str(session_id)]))

        self.manager.database.set_user_session(session_id, user_hash);
        puzzle = json.loads(self.manager.database.select_puzzle(int(puzzle_id))["JSON"])
        return self.__get_template("crossword.mako").render(
                base=self.url_base,
                puzzle=puzzle,
                clues=json.dumps(puzzle["clues"]))

    @cherrypy.expose
    def victory(self):
        return self.__get_template("victory.mako").render(base=self.url_base)

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
    def crypto(self):
        return self.__get_template("crypto.mako").render(
                base=self.url_base)

    @cherrypy.expose
    def json(self, type, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        result = None
        if type == "move":
            x = int(kwargs['cord_x'])
            y = int(kwargs['cord_y'])
            char = kwargs['char']
            session_id = kwargs['session_id']
            self.manager.database.insert_move(session_id, self.valid_hash(), x, y, char, datetime.datetime.utcnow())

        elif type == "moves":
            session_id = kwargs['session_id']
            since = kwargs['since']
            moves, i = [], 0
            while i < 10:
                i += 1
                moves = self.manager.database.select_move(session_id, int(since))
                if len(moves) == 0:
                    time.sleep(1)
                else:
                    break
            result = json.dumps(moves)
        return result

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def js(self, *args):
        path = '/'.join(filter(lambda a: not a == "..", args))
        cherrypy.response.headers['Content-Type'] = 'text/javascript'
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return open(os.path.join(self.base_path, "html", "js", path))


    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def css(self, *args):
        path = '/'.join(filter(lambda a: not a == "..", args))
        cherrypy.response.headers['Content-Type'] = 'text/css'
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return open(os.path.join(self.base_path, "html", "css", path))

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def audio(self, path=None):
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return serve_file(os.path.join(self.base_path, "html", "audio", path))

    @cherrypy.expose
    #@cherrypy.tools.caching(delay=300)
    @cherrypy.tools.etags(autotags=True)
    def images(self, path=None):
        cherrypy.response.headers['Cache-Control'] = self.cache_string
        return serve_file(os.path.join(self.base_path, "html", "images", path))

try:
    print "launching"
    current_directory = os.path.dirname(os.path.realpath(__file__))

    settings_file = os.path.join(current_directory, "settings.json")
    settings = { "url_base" : "/", "port" : 4567 }

    if os.path.exists(settings_file):
        with open(settings_file, 'r') as settings_obj:
            settings = json.load(settings_obj)
    else:
        with open(settings_file, 'w') as settings_obj:
            json.dump(settings, settings_obj, sort_keys=True, indent=1)

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
            , 'server.socket_port': settings["port"]
            , 'thread_pool': 100
        })
    host_process = Host(current_directory, settings["url_base"])
    cherrypy.tree.mount(host_process, config=app_config)
    cherrypy.engine.start()
    print "launched"
    cherrypy.engine.block()
except Exception as e:
    print e
finally:
    if host_process:
        host_process.__del__()
