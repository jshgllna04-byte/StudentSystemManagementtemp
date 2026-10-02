import sqlite3
import json

DATABASE = "student.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            year_level TEXT NOT NULL,
            subjects TEXT
        )
    """)

    connection.commit()
    connection.close()


def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?,?)
        """, (username, password))

        connection.commit()
        connection.close()

        return True

    except sqlite3.IntegrityError:

        connection.close()

        return False


def authentication(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    return user


def add_student(
    fullname,
    age,
    address,
    contact,
    email,
    course,
    year_level,
    subjects
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students(
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level,
            subjects
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        fullname,
        age,
        address,
        contact,
        email,
        course,
        year_level,
        json.dumps(subjects)
    ))

    connection.commit()

    student_id = cursor.lastrowid

    connection.close()

    return student_id


def get_all_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return students


def get_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year_level,
            subjects
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return student


def update_student(
    student_id,
    fullname,
    age,
    address,
    contact,
    email,
    course,
    year_level,
    subjects
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET
            fullname = ?,
            age = ?,
            address = ?,
            contact = ?,
            email = ?,
            course = ?,
            year_level = ?,
            subjects = ?
        WHERE id = ?
    """, (
        fullname,
        age,
        address,
        contact,
        email,
        course,
        year_level,
        json.dumps(subjects),
        student_id
    ))

    connection.commit()
    connection.close()


def delete_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    connection.commit()
    connection.close()