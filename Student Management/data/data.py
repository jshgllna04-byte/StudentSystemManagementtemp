import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "student.db"

USERS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
"""

STUDENTS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        age INTEGER NOT NULL,
        address TEXT NOT NULL,
        contact TEXT NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL,
        year_level TEXT NOT NULL
    )
"""


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(USERS_SCHEMA)
    cursor.execute(STUDENTS_SCHEMA)

    connection.commit()
    connection.close()
