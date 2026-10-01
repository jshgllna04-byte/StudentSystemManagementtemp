import sqlite3

from data.data import connection_scope

INSERT_USER = """
    INSERT INTO USER (user_name, password) VALUES (?,?)
"""

SELECT_USER = """
    SELECT user_id, user_name FROM USER WHERE user_name = ? AND password = ?
"""


def insert_user(user_name, password):
    with connection_scope() as connection:
        try:
            connection.execute(INSERT_USER, (user_name, password))
        except sqlite3.IntegrityError:
            return False

    return True


def select_user(user_name, password):
    with connection_scope() as connection:
        return connection.execute(
            SELECT_USER,
            (user_name, password),
        ).fetchone()
