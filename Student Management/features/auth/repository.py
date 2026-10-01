import sqlite3

from data.data import get_connection

INSERT_USER = """
    INSERT INTO users (username, password) VALUES (?,?)
"""

SELECT_USER = """
    SELECT id, username FROM users WHERE username = ? AND password = ?
"""


def insert_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(INSERT_USER, (username, password))
        connection.commit()

        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def select_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(SELECT_USER, (username, password))

    user = cursor.fetchone()

    connection.close()

    return user
