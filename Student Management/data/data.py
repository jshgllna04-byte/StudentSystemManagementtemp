import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "student.db"

USERS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS USER(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
"""

COURSE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS COURSE(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT UNIQUE NOT NULL,
        course_name TEXT NOT NULL
    )
"""

STUDENT_INFO_SCHEMA = """
    CREATE TABLE IF NOT EXISTS STUDENT_INFO(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        student_number TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        course_id INTEGER NOT NULL,
        year_level TEXT NOT NULL,
        address TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES USER(user_id),
        FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
    )
"""

ENROLLMENT_SCHEMA = """
    CREATE TABLE IF NOT EXISTS ENROLLMENT(
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        time TEXT NOT NULL,
        room TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES STUDENT_INFO(student_id),
        FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
    )
"""


def get_connection():
    return sqlite3.connect(DATABASE)


@contextmanager
def connection_scope():
    # Guarantees the connection is always closed, so a failed statement
    # cannot leak an open transaction and lock the database.
    connection = sqlite3.connect(DATABASE)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def table_exists(cursor, name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (name,),
    )
    return cursor.fetchone() is not None


def seed_courses(cursor):
    programs = [
        ("BSCS", "Bachelor of Science in Computer Science"),
        ("BSIT", "Bachelor of Science in Information Technology"),
        ("BSCpE", "Bachelor of Science in Computer Engineering"),
    ]

    for course_code, course_name in programs:
        cursor.execute(
            """
            INSERT OR IGNORE INTO COURSE (course_code, course_name)
            VALUES (?, ?)
            """,
            (course_code, course_name),
        )


def migrate_legacy_users(cursor):
    # The legacy users table has id/username columns, so it is copied
    # into the new USER table rather than renamed.
    if not table_exists(cursor, "users"):
        return

    cursor.execute(
        """
        INSERT OR IGNORE INTO USER (user_name, password)
        SELECT username, password FROM users
        """
    )

    cursor.execute("DROP TABLE users")


def migrate_legacy_students(cursor):
    if not table_exists(cursor, "students"):
        return

    cursor.execute(
        """
        SELECT COUNT(*) FROM STUDENT_INFO
        """
    )
    already_migrated = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students")
    legacy_count = cursor.fetchone()[0]

    if already_migrated == 0 and legacy_count > 0:
        cursor.execute(
            """
            INSERT INTO STUDENT_INFO(
                student_id, user_id, student_number, full_name,
                course_id, year_level, address, contact_number, email, age
            )
            SELECT
                s.id,
                NULL,
                CAST(s.id AS TEXT),
                s.fullname,
                COALESCE(
                    (SELECT course_id FROM COURSE WHERE course_code = s.course),
                    (SELECT MIN(course_id) FROM COURSE)
                ),
                s.year_level,
                s.address,
                s.contact,
                s.email,
                s.age
            FROM students s
            """
        )

    cursor.execute("DROP TABLE students")


def relax_user_id_unique(cursor):
    # An earlier build declared user_id UNIQUE, which limited each account
    # to a single student. Rebuild the table without it (1 user : N students).
    cursor.execute("PRAGMA index_list(STUDENT_INFO)")

    for index in cursor.fetchall():
        # (seq, name, unique, origin, partial)
        if not index[2]:
            continue

        cursor.execute(f"PRAGMA index_info('{index[1]}')")

        columns = [row[2] for row in cursor.fetchall()]

        if columns != ["user_id"]:
            continue

        cursor.execute("DROP TABLE IF EXISTS STUDENT_INFO_rebuild")
        cursor.execute(
            """
            CREATE TABLE STUDENT_INFO_rebuild(
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                student_number TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                year_level TEXT NOT NULL,
                address TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(course_id) REFERENCES COURSE(course_id)
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO STUDENT_INFO_rebuild(
                student_id, user_id, student_number, full_name,
                course_id, year_level, address, contact_number, email, age
            )
            SELECT
                student_id, user_id, student_number, full_name,
                course_id, year_level, address, contact_number, email, age
            FROM STUDENT_INFO
            """
        )

        cursor.execute("DROP TABLE STUDENT_INFO")
        cursor.execute("ALTER TABLE STUDENT_INFO_rebuild RENAME TO STUDENT_INFO")
        return


def create_database():
    with connection_scope() as connection:
        cursor = connection.cursor()

        cursor.execute(USERS_SCHEMA)
        migrate_legacy_users(cursor)

        cursor.execute(COURSE_SCHEMA)
        seed_courses(cursor)

        cursor.execute(STUDENT_INFO_SCHEMA)
        relax_user_id_unique(cursor)
        migrate_legacy_students(cursor)

        cursor.execute(ENROLLMENT_SCHEMA)
