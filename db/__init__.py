import os
import sqlite3
import uuid
import datetime

epoch = datetime.datetime(1970, 1, 1)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def generate_id():
    return uuid.uuid4().int

def get_timestamp(dt):
    return int((dt - epoch).total_seconds())

def from_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts)

def first_or_none(rows):
    return rows[0] if len(rows) > 0 else None

def last_or_none(rows):
    return rows[-1] if len(rows) > 0 else None

class DB(object):
    last_id = None

    def __init__(self, db_file):
        self._db_file = db_file
        self.__initialize_db()

    def __del__(self):
        return

    def __initialize_db(self):
        if not os.path.exists(self._db_file):
            self.execute_sql("CREATE TABLE Session (Id INTEGER PRIMARY KEY, PuzzleId INTEGER )")
            self.execute_sql("CREATE TABLE Puzzle (Id INTEGER PRIMARY KEY, Title TEXT, Timestamp INTEGER , JSON TEXT)")
            self.execute_sql("CREATE TABLE User_Session (SessionId INTEGER, UserId INTEGER)")
            self.execute_sql("CREATE TABLE User (Id INTEGER PRIMARY KEY, Username TEXT UNIQUE, LastAccessed INTEGER )")
            self.execute_sql("CREATE TABLE Move (Id INTEGER PRIMARY KEY, SessionId INTEGER , UserId INTEGER , Date INTEGER, X INTEGER, Y INTEGER, Letter CHAR )")
            return
        return self._db_file

    def execute_sql(self, sql, parameters=None):
        rows = None
        try:
            if self._db_file:
                connection = None
                try:
                    connection = sqlite3.connect(self._db_file, timeout=30)
                    connection.row_factory = dict_factory
                    cursor = connection.cursor()
                    if not parameters:
                        rows = cursor.execute(sql).fetchall()
                    else:
                        rows = cursor.execute(sql, parameters).fetchall()
                    connection.commit()
                    if cursor.lastrowid: self.last_id = cursor.lastrowid
                except Exception as e:
                    connection.rollback()
                    raise e
                finally:
                    if connection:
                        connection.close()

            return rows
        except Exception as e:
            raise e

    def insert_puzzle(self, title, timestamp, json):
        query = "insert into puzzle (Title, Timestamp, JSON) values (?, ?, ?)"
        parameters = (title, timestamp, json,)
        self.execute_sql(query, parameters)

    def select_puzzle(self, puzzle_id):
        query = "select id, title, timestamp, json from puzzle where id = ?"
        return first_or_none(self.execute_sql(query, (puzzle_id,)))

    def select_puzzles(self):
        query = "select id, title, timestamp from puzzle"
        return self.execute_sql(query)

    def select_user(self, username):
        query = "select * from user where username = ?"
        return first_or_none(self.execute_sql(query, (username,)))

    def insert_user(self, username):
        query = "insert into user (Username, LastAccessed) values (?, ?)"
        self.execute_sql(query, (username, get_timestamp(datetime.datetime.utcnow(),)))
        return self.last_id

    def insert_session(self, puzzle_id, username):
        query = "insert into session (PuzzleId) values (?)"
        self.execute_sql(query, (puzzle_id,))
        session_id = self.last_id
        self.set_user_session(session_id, username)
        return session_id

    def insert_move(self, session_id, username, x, y, char, date):
        user_id = self.select_user(username)['Id']
        query = "insert into move (SessionId, UserId, Date, X, Y, Letter) values (?, ?, ?, ?, ?, ?)"
        self.execute_sql(query, (session_id, user_id, get_timestamp(date), x, y, char,))

    def select_move(self, session_id, since):
        query = "select * from move where SessionId = ? and Id > ? order by Id asc"
        return self.execute_sql(query, (session_id, since, ))

    def get_user_session(self, puzzle_id, username):
        user_id = self.select_user(username)['Id']

        query  = "select us.SessionId "
        query += "from user_session us "
        query += "join session s on s.Id = us.SessionId "
        query += "where us.UserId = ? and s.PuzzleId = ?"

        result = last_or_none(self.execute_sql(query, (user_id, puzzle_id,)))

        return result["SessionId"] if result else None

    def set_user_session(self, session_id, username):
        user_id = self.select_user(username)['Id']
        query = "select SessionId from user_session where SessionId = ? and UserId = ?"
        if len(self.execute_sql(query, (session_id, user_id,))) == 0:
            query = "insert into user_session (SessionId, UserId) values (?, ?)"
            self.execute_sql(query, (session_id, user_id,))
        return

