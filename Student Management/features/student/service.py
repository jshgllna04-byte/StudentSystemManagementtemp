from features.student import repository

REQUIRED_FIELDS = [
    ("fullname", "Please enter the fullname."),
    ("age", "Please enter the age."),
    ("address", "Please enter the address."),
    ("contact", "Please enter the contact."),
    ("email", "Please enter the email.")
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


def create(data):
    title, message = validate(data)

    if title:
        return None, title, message

    student_id = repository.insert_student(
        data["fullname"],
        int(data["age"]),
        data["address"],
        data["contact"],
        data["email"],
        data["course"],
        data["year_level"]
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

    repository.update_student(
        student_id,
        data["fullname"],
        int(data["age"]),
        data["address"],
        data["contact"],
        data["email"],
        data["course"],
        data["year_level"]
    )

    return True, None, None


def delete(student_id):
    repository.delete_student(student_id)
