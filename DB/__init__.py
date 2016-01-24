import sqlite3

class DB(object):
    _db_file = None
    _db_lock = None
    _last_id = None

    def __init__(self, db_file):
        self._db_file = db_file
        self.__initialize_db()

    def __initialize_db(self):
        return self._db_file

    def execute_sql(self, sql, parameters=None):
        rows = None
        try:
            if self._db_file:
                connection = None
                try:
                    connection = sqlite3.connect(self._db_file, timeout=30)
                    connection.row_factory = sqlite3.Row
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
