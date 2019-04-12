import os
import sqlite3
import uuid
import datetime
import hashlib

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


def hash_string(string, salt):
    sha1 = hashlib.sha1()
    sha1.update(str(string))
    if salt:
        sha1.update(str(salt))
    return sha1.hexdigest()


class DB(object):
    last_id = None
    salt = None

    def __init__(self, db_file, salt="CCCP"):
        self._db_file = db_file
        self.__initialize_db()
        self.salt = salt

    def __del__(self):
        return

    def __initialize_db(self):
        if not os.path.exists(self._db_file):
            self.execute_sql("CREATE TABLE Session (Id INTEGER PRIMARY KEY, PuzzleId INTEGER )")
            self.execute_sql("CREATE TABLE Puzzle (Id INTEGER PRIMARY KEY, Title TEXT, Timestamp INTEGER , JSON TEXT)")
            self.execute_sql("CREATE TABLE User_Session (SessionId INTEGER, UserHash TEXT)")
            self.execute_sql("CREATE TABLE User (Id INTEGER PRIMARY KEY, Username TEXT, Email TEXT UNIQUE, Password TEXT, LastAccessed INTEGER )")
            self.execute_sql("CREATE TABLE Move (Id INTEGER PRIMARY KEY, SessionId INTEGER , UserHash TEXT, Date INTEGER, X INTEGER, Y INTEGER, Letter CHAR )")
            return
        return self._db_file

    def hash(self, string):
        return hash_string(string, self.salt)

    def execute_sql(self, sql, parameters=None):
        rows = None
        try:
            if self._db_file:
                connection = None
                try:
                    connection = sqlite3.connect(self._db_file, timeout=30)
                    connection.row_factory = dict_factory
                    connection.create_function("HASH", 1, self.hash)
                    cursor = connection.cursor()
                    if not parameters:
                        rows = cursor.execute(sql).fetchall()
                    else:
                        rows = cursor.execute(sql, parameters).fetchall()
                    connection.commit()
                    if cursor.lastrowid: self.last_id = cursor.lastrowid
                except Exception as e:
                    if connection:
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

    def select_user(self, userhash):
        query = "select hash(id) Hash, username from user where hash(id) = ?"
        return first_or_none(self.execute_sql(query, (userhash,)))

    def select_user_by_email(self, email):
        query = "select hash(id) Hash from user where email = hash(?) "
        return first_or_none(self.execute_sql(query, (email,)))

    def login(self, email, password):
        password = email+password
        query = "select hash(id) Hash from user where email = hash(?) and password = hash(?)"
        row = first_or_none(self.execute_sql(query, (email, password,)))
        return row['Hash'] if row else None

    def insert_user(self, username, email, password):
        password = email+password
        query = "insert into user (Username, Email, Password, LastAccessed) values (?, hash(?), hash(?), ?)"
        self.execute_sql(query, (username, email, password, get_timestamp(datetime.datetime.utcnow(),)))
        return self.hash(self.last_id)

    def insert_session(self, puzzle_id, userhash):
        query = "insert into session (PuzzleId) values (?)"
        self.execute_sql(query, (puzzle_id,))
        session_id = self.last_id
        self.set_user_session(session_id, userhash)
        return session_id

    def insert_move(self, session_id, userhash, x, y, char, date):
        user = self.select_user(userhash)
        if user:
            query = "insert into move (SessionId, UserHash, Date, X, Y, Letter) values (?, ?, ?, ?, ?, ?)"
            self.execute_sql(query, (session_id, userhash, get_timestamp(date), x, y, char,))

    def select_move(self, session_id, since):
        query = "select m.*, u.Username from move m join user u on m.UserHash = hash(u.Id) where m.SessionId = ? and m.Id > ? order by Id asc"
        return self.execute_sql(query, (session_id, since, ))

    def get_user_session(self, puzzle_id, userhash):
        user = self.select_user(userhash)
        if user:
            query = "select us.SessionId "
            query += "from user_session us "
            query += "join session s on s.Id = us.SessionId "
            query += "where us.UserHash = ? and s.PuzzleId = ?"

            result = last_or_none(self.execute_sql(query, (userhash, puzzle_id,)))

            return result["SessionId"] if result else None

    def set_user_session(self, session_id, userhash):
        user = self.select_user(userhash)
        if user:
            query = "select SessionId from user_session where SessionId = ? and UserHash = ?"
            if len(self.execute_sql(query, (session_id, userhash,))) == 0:
                query = "insert into user_session (SessionId, UserHash) values (?, ?)"
                self.execute_sql(query, (session_id, userhash,))


