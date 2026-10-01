from data.data import connection_scope

SELECT_COURSES = """
    SELECT course_id, course_code, course_name
    FROM COURSE
    ORDER BY course_id
"""

SELECT_COURSE_ID = """
    SELECT course_id FROM COURSE WHERE course_code = ?
"""

INSERT_STUDENT = """
    INSERT INTO STUDENT_INFO (
        user_id, student_number, full_name, course_id,
        year_level, address, contact_number, email, age
    ) VALUES (?,?,?,?,?,?,?,?,?)
"""

SELECT_ALL_STUDENTS = """
    SELECT
        s.student_id,
        s.user_id,
        s.student_number,
        s.full_name,
        c.course_code,
        s.year_level,
        s.address,
        s.contact_number,
        s.email,
        s.age
    FROM STUDENT_INFO s
    JOIN COURSE c ON c.course_id = s.course_id
    ORDER BY s.student_id DESC
"""

SELECT_STUDENT_BY_NUMBER = """
    SELECT student_id FROM STUDENT_INFO WHERE student_number = ?
"""

SELECT_STUDENT = """
    SELECT
        s.student_id,
        s.user_id,
        s.student_number,
        s.full_name,
        c.course_code,
        s.year_level,
        s.address,
        s.contact_number,
        s.email,
        s.age
    FROM STUDENT_INFO s
    JOIN COURSE c ON c.course_id = s.course_id
    WHERE s.student_id = ?
"""

UPDATE_STUDENT = """
    UPDATE STUDENT_INFO
    SET student_number = ?, full_name = ?, course_id = ?, year_level = ?,
        address = ?, contact_number = ?, email = ?, age = ?
    WHERE student_id = ?
"""

DELETE_STUDENT = """
    DELETE FROM STUDENT_INFO WHERE student_id = ?
"""

INSERT_ENROLLMENT = """
    INSERT INTO ENROLLMENT (student_id, course_id, code, time, room)
    VALUES (?,?,?,?,?)
"""

SELECT_ENROLLMENTS = """
    SELECT
        e.enrollment_id,
        e.student_id,
        c.course_code,
        e.code,
        e.time,
        e.room
    FROM ENROLLMENT e
    JOIN COURSE c ON c.course_id = e.course_id
    WHERE e.student_id = ?
    ORDER BY e.enrollment_id
"""

DELETE_ENROLLMENT = """
    DELETE FROM ENROLLMENT WHERE enrollment_id = ?
"""


def select_courses():
    with connection_scope() as connection:
        return connection.execute(SELECT_COURSES).fetchall()


def select_course_id(course_code):
    with connection_scope() as connection:
        row = connection.execute(SELECT_COURSE_ID, (course_code,)).fetchone()

    return row[0] if row else None


def insert_student(user_id, student_number, full_name, course_id, year_level, address, contact_number, email, age):
    with connection_scope() as connection:
        cursor = connection.execute(
            INSERT_STUDENT,
            (
                user_id,
                student_number,
                full_name,
                course_id,
                year_level,
                address,
                contact_number,
                email,
                age,
            ),
        )

        return cursor.lastrowid


def select_all_students():
    with connection_scope() as connection:
        return connection.execute(SELECT_ALL_STUDENTS).fetchall()


def select_student_by_number(student_number):
    with connection_scope() as connection:
        row = connection.execute(
            SELECT_STUDENT_BY_NUMBER,
            (student_number,),
        ).fetchone()

    return row[0] if row else None


def select_student(student_id):
    with connection_scope() as connection:
        return connection.execute(SELECT_STUDENT, (student_id,)).fetchone()


def update_student(student_id, student_number, full_name, course_id, year_level, address, contact_number, email, age):
    with connection_scope() as connection:
        connection.execute(
            UPDATE_STUDENT,
            (
                student_number,
                full_name,
                course_id,
                year_level,
                address,
                contact_number,
                email,
                age,
                student_id,
            ),
        )


def delete_student(student_id):
    with connection_scope() as connection:
        connection.execute(DELETE_STUDENT, (student_id,))


def insert_enrollment(student_id, course_id, code, time, room):
    with connection_scope() as connection:
        cursor = connection.execute(
            INSERT_ENROLLMENT,
            (student_id, course_id, code, time, room),
        )

        return cursor.lastrowid


def select_enrollments(student_id):
    with connection_scope() as connection:
        return connection.execute(SELECT_ENROLLMENTS, (student_id,)).fetchall()


def delete_enrollment(enrollment_id):
    with connection_scope() as connection:
        connection.execute(DELETE_ENROLLMENT, (enrollment_id,))
