from features.student import repository

REQUIRED_FIELDS = [
    ("student_number", "Please enter the student number."),
    ("full_name", "Please enter the full name."),
    ("age", "Please enter the age."),
    ("address", "Please enter the address."),
    ("contact_number", "Please enter the contact number."),
    ("email", "Please enter the email."),
]


def validate(data):
    for field, message in REQUIRED_FIELDS:
        if not data.get(field):
            return "Missing Information", message

    try:
        age = int(data["age"])

        if age <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return "Invalid Age", "Age must be a valid number"

    return None, None


def get_courses():
    return repository.select_courses()


def get_course_codes():
    return [course[1] for course in repository.select_courses()]


def get_course_id(course_code):
    return repository.select_course_id(course_code)


def number_taken(student_number, student_id=None):
    existing = repository.select_student_by_number(student_number)

    return existing is not None and existing != student_id


def create(user_id, data):
    title, message = validate(data)

    if title:
        return None, title, message

    course_id = get_course_id(data["course_code"])

    if course_id is None:
        return None, "Invalid Course", "Please select a valid course."

    if number_taken(data["student_number"]):
        return (
            None,
            "Student Number Exists",
            "That student number is already registered.",
        )

    student_id = repository.insert_student(
        user_id,
        data["student_number"],
        data["full_name"],
        course_id,
        data["year_level"],
        data["address"],
        data["contact_number"],
        data["email"],
        int(data["age"]),
    )

    return student_id, None, None


def get_all():
    return repository.select_all_students()


def get_one(student_id):
    return repository.select_student(student_id)


def update(student_id, data):
    title, message = validate(data)

    if title:
        return False, title, message

    course_id = get_course_id(data["course_code"])

    if course_id is None:
        return False, "Invalid Course", "Please select a valid course."

    if number_taken(data["student_number"], student_id):
        return (
            False,
            "Student Number Exists",
            "That student number is already registered.",
        )

    repository.update_student(
        student_id,
        data["student_number"],
        data["full_name"],
        course_id,
        data["year_level"],
        data["address"],
        data["contact_number"],
        data["email"],
        int(data["age"]),
    )

    return True, None, None


def delete(student_id):
    for enrollment in repository.select_enrollments(student_id):
        repository.delete_enrollment(enrollment[0])

    repository.delete_student(student_id)


def enroll(student_id, course_code, code, time, room):
    if not code or not time or not room:
        return None, "Missing Information", "Please fill in all enrollment fields."

    course_id = get_course_id(course_code)

    if course_id is None:
        return None, "Invalid Course", "Please select a valid course."

    enrollment_id = repository.insert_enrollment(
        student_id,
        course_id,
        code,
        time,
        room,
    )

    return enrollment_id, None, None


def get_enrollments(student_id):
    return repository.select_enrollments(student_id)


def unenroll(enrollment_id):
    repository.delete_enrollment(enrollment_id)
