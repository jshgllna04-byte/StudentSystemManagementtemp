from data.data import get_connection

INSERT_STUDENT = """
    INSERT INTO students (
        fullname,age,address,contact,email,course,year_level
    ) VALUES (?,?,?,?,?,?,?)
"""

SELECT_ALL_STUDENTS = """
    SELECT id, fullname, age, address, contact, email, course, year_level
    FROM students
    ORDER BY id DESC
"""

SELECT_STUDENT = """
    SELECT id,fullname,age, address, contact, email, course, year_level
    FROM students
    WHERE id = ?
"""

UPDATE_STUDENT = """
    UPDATE students
    SET fullname = ?, age = ?, address = ?, contact = ?, email = ?,
        course = ?, year_level = ?
    WHERE id = ?
"""

DELETE_STUDENT = """
    DELETE FROM students
    WHERE id = ?
"""


def insert_student(fullname, age, address, contact, email, course, year_level):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        INSERT_STUDENT,
        (fullname, age, address, contact, email, course, year_level)
    )

    connection.commit()
    student_id = cursor.lastrowid
    connection.close()

    return student_id


def select_all_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(SELECT_ALL_STUDENTS)

    students = cursor.fetchall()
    connection.close()

    return students


def select_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(SELECT_STUDENT, (student_id,))

    student = cursor.fetchone()
    connection.close()

    return student


def update_student(student_id, fullname, age, address, contact, email, course, year_level):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        UPDATE_STUDENT,
        (fullname, age, address, contact, email, course, year_level, student_id)
    )

    connection.commit()
    connection.close()


def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(DELETE_STUDENT, (student_id,))

    connection.commit()
    connection.close()
