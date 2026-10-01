from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox
)

from features.student import service
from features.student.model import YEAR_LEVELS, get_subjects


class StudentFormMixin:

    def load_course_choices(self):
        course_codes = service.get_course_codes()

        self.course.clear()
        self.course.addItems(course_codes)

        if hasattr(self, "enroll_course"):
            self.enroll_course.clear()
            self.enroll_course.addItems(course_codes)

    def update_subjects(self):
        self.subjects.clear()

        for subject in get_subjects(
            self.course.currentText(),
            self.year_level.currentText()
        ):
            self.subjects.addItem("• " + subject)

    def read_form(self):
        return {
            "student_number": self.student_number.text().strip(),
            "full_name": self.full_name.text().strip(),
            "age": self.age.text().strip(),
            "address": self.address.text().strip(),
            "contact_number": self.contact.text().strip(),
            "email": self.email.text().strip(),
            "course_code": self.course.currentText(),
            "year_level": self.year_level.currentText()
        }

    def fill_form(self, student):
        # STUDENT_COLUMNS order
        self.student_number.setText(student[2])
        self.full_name.setText(student[3])

        course_index = self.course.findText(student[4])
        if course_index >= 0:
            self.course.setCurrentIndex(course_index)

        year_index = self.year_level.findText(student[5])
        if year_index >= 0:
            self.year_level.setCurrentIndex(year_index)

        self.address.setText(student[6])
        self.contact.setText(student[7])
        self.email.setText(student[8])
        self.age.setText(str(student[9]))


class AddStudentPage(StudentFormMixin, QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        backbtn = QPushButton("Back")
        backbtn.setObjectName("back")
        backbtn.clicked.connect(self.main_window.show_dashboard)
        top_layout.addWidget(backbtn)

        title = QLabel("Add student")
        title.setObjectName("pageTitle")

        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        form = QGridLayout()

        self.student_number = QLineEdit()
        self.student_number.setPlaceholderText("Enter Student Number")

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Enter Full Name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter age")

        self.address = QLineEdit()
        self.address.setPlaceholderText("Enter Address")

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Enter Contact Number")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email")

        self.course = QComboBox()

        self.year_level = QComboBox()
        self.year_level.addItems(YEAR_LEVELS)

        self.subjects = QListWidget()

        form.addWidget(QLabel("Student Number"), 0, 0)
        form.addWidget(self.student_number, 1, 0)

        form.addWidget(QLabel("Full Name"), 0, 1)
        form.addWidget(self.full_name, 1, 1)

        form.addWidget(QLabel("Age"), 2, 0)
        form.addWidget(self.age, 3, 0)

        form.addWidget(QLabel("Address"), 2, 1)
        form.addWidget(self.address, 3, 1)

        form.addWidget(QLabel("Contact Number"), 4, 0)
        form.addWidget(self.contact, 5, 0)

        form.addWidget(QLabel("Email"), 4, 1)
        form.addWidget(self.email, 5, 1)

        form.addWidget(QLabel("Course"), 6, 0)
        form.addWidget(self.course, 7, 0)

        form.addWidget(QLabel("Year Level"), 6, 1)
        form.addWidget(self.year_level, 7, 1)

        form.addWidget(QLabel("Subjects"), 8, 0, 1, 2)

        main_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        nextbtn = QPushButton("Next>")
        nextbtn.setFixedWidth(150)
        nextbtn.clicked.connect(self.next_page)

        btn_layout.addWidget(nextbtn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        self.course.currentIndexChanged.connect(self.update_subjects)
        self.year_level.currentIndexChanged.connect(self.update_subjects)

        self.load_course_choices()
        self.update_subjects()

    def clear_form(self):
        self.student_number.clear()
        self.full_name.clear()
        self.age.clear()
        self.address.clear()
        self.contact.clear()
        self.email.clear()

        self.load_course_choices()
        self.year_level.setCurrentIndex(0)
        self.update_subjects()

    def next_page(self):
        data = self.read_form()

        title, message = service.validate(data)

        if title:
            QMessageBox.warning(self, title, message)
            return

        self.main_window.pending_student = data

        self.main_window.verify_page.load_data(data)
        self.main_window.show_verify()


class VerifyStudentPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Verify")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        form = QGridLayout()

        self.student_number = QLabel()
        self.full_name = QLabel()
        self.age = QLabel()
        self.address = QLabel()
        self.contact = QLabel()
        self.email = QLabel()

        self.course = QLabel()
        self.year_level = QLabel()

        self.subjects = QListWidget()

        # Left side
        form.addWidget(QLabel("Student Number:"), 0, 0)
        form.addWidget(self.student_number, 0, 1)

        form.addWidget(QLabel("Full Name:"), 1, 0)
        form.addWidget(self.full_name, 1, 1)

        form.addWidget(QLabel("Age:"), 2, 0)
        form.addWidget(self.age, 2, 1)

        form.addWidget(QLabel("Address:"), 3, 0)
        form.addWidget(self.address, 3, 1)

        form.addWidget(QLabel("Contact Number:"), 4, 0)
        form.addWidget(self.contact, 4, 1)

        form.addWidget(QLabel("Email:"), 5, 0)
        form.addWidget(self.email, 5, 1)

        # Right side
        form.addWidget(QLabel("Course:"), 0, 2)
        form.addWidget(self.course, 0, 3)

        form.addWidget(QLabel("Year Level:"), 0, 4)
        form.addWidget(self.year_level, 0, 5)

        form.addWidget(QLabel("Subjects:"), 1, 2)
        form.addWidget(self.subjects, 1, 3, 5, 3)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_add_student)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        buttons.addStretch()
        buttons.addWidget(back_button)
        buttons.addWidget(submit_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self.setLayout(layout)

    def load_data(self, data):
        self.student_number.setText(data["student_number"])
        self.full_name.setText(data["full_name"])
        self.age.setText(str(data["age"]))
        self.address.setText(data["address"])
        self.contact.setText(data["contact_number"])
        self.email.setText(data["email"])
        self.course.setText(data["course_code"])
        self.year_level.setText(data["year_level"])

        self.subjects.clear()

        for subject in get_subjects(data["course_code"], data["year_level"]):
            self.subjects.addItem("• " + subject)

    def submit(self):
        data = self.main_window.pending_student

        if not data:
            return

        user_id = self.main_window.current_user[0]

        student_id, title, message = service.create(user_id, data)

        if title:
            QMessageBox.warning(self, title, message)
            return

        QMessageBox.information(
            self,
            "Success",
            "Student added successfully!"
        )

        self.main_window.pending_student = None

        self.main_window.show_dashboard()


class ViewStudentPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.students = []

        layout = QVBoxLayout()

        # ----------------------------------------------------
        # TOP
        # ----------------------------------------------------

        top = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setObjectName("back")
        back_button.setFixedWidth(80)
        back_button.clicked.connect(self.main_window.show_dashboard)

        title = QLabel("Students Information")
        title.setObjectName("sectionTitle")

        top.addWidget(back_button)
        top.addWidget(title)
        top.addStretch()

        layout.addLayout(top)

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search student...")
        self.search.textChanged.connect(self.search_students)

        layout.addWidget(self.search)

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        self.table = QTableWidget()
        self.table.setColumnCount(10)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Student Number",
            "Name",
            "Course",
            "Year Level",
            "Address",
            "Contact",
            "Email",
            "Age",
            "View"
        ])

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_students(self):
        self.search.clear()

        self.students = service.get_all()

        self.display_students(self.students)

    def display_students(self, students):
        self.table.setRowCount(0)

        # STUDENT_COLUMNS -> table column order
        indexes = [0, 2, 3, 4, 5, 6, 7, 8, 9]

        for row, student in enumerate(students):
            self.table.insertRow(row)

            for column, index in enumerate(indexes):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(student[index]))
                )

            view_button = QPushButton("View")
            view_button.setObjectName("view")

            view_button.clicked.connect(
                lambda checked=False, student_id=student[0]:
                self.open_student(student_id)
            )

            self.table.setCellWidget(row, 9, view_button)

    def search_students(self, text):
        text = text.lower().strip()

        if not text:
            self.display_students(self.students)
            return

        filtered = []

        for student in self.students:
            student_number = str(student[2]).lower()
            name = str(student[3]).lower()
            email = str(student[8]).lower()

            if text in student_number or text in name or text in email:
                filtered.append(student)

        self.display_students(filtered)

    def open_student(self, student_id):
        self.main_window.show_student_details(student_id)


class StudentDetailsPage(StudentFormMixin, QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.student_id = None

        layout = QVBoxLayout()

        # ----------------------------------------------------
        # TOP
        # ----------------------------------------------------

        top = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setObjectName("back")
        back_button.setFixedWidth(80)
        back_button.clicked.connect(self.main_window.show_students)

        title = QLabel("Student Information")
        title.setObjectName("pageTitle")

        top.addWidget(back_button)
        top.addWidget(title)
        top.addStretch()

        layout.addLayout(top)

        # ----------------------------------------------------
        # FORM
        # ----------------------------------------------------

        form = QGridLayout()

        self.student_number = QLineEdit()
        self.full_name = QLineEdit()
        self.age = QLineEdit()
        self.address = QLineEdit()
        self.contact = QLineEdit()
        self.email = QLineEdit()

        self.course = QComboBox()
        self.year_level = QComboBox()
        self.year_level.addItems(YEAR_LEVELS)

        self.subjects = QListWidget()

        form.addWidget(QLabel("Student Number"), 0, 0)
        form.addWidget(self.student_number, 1, 0)

        form.addWidget(QLabel("Full Name"), 0, 1)
        form.addWidget(self.full_name, 1, 1)

        form.addWidget(QLabel("Age"), 2, 0)
        form.addWidget(self.age, 3, 0)

        form.addWidget(QLabel("Address"), 2, 1)
        form.addWidget(self.address, 3, 1)

        form.addWidget(QLabel("Contact Number"), 4, 0)
        form.addWidget(self.contact, 5, 0)

        form.addWidget(QLabel("Email"), 4, 1)
        form.addWidget(self.email, 5, 1)

        form.addWidget(QLabel("Course"), 6, 0)
        form.addWidget(self.course, 7, 0)

        form.addWidget(QLabel("Year Level"), 6, 1)
        form.addWidget(self.year_level, 7, 1)

        form.addWidget(QLabel("Subjects"), 8, 0, 1, 2)

        layout.addLayout(form)

        # ----------------------------------------------------
        # ENROLLMENT
        # ----------------------------------------------------

        enrollment_title = QLabel("Enrollments")
        enrollment_title.setObjectName("sectionTitle")

        layout.addWidget(enrollment_title)

        self.enrollment_table = QTableWidget()
        self.enrollment_table.setColumnCount(5)

        self.enrollment_table.setHorizontalHeaderLabels([
            "Course",
            "Code",
            "Time",
            "Room",
            "Action"
        ])

        self.enrollment_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.enrollment_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.enrollment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.enrollment_table)

        enrollment_form = QGridLayout()

        self.enroll_course = QComboBox()

        self.enroll_code = QLineEdit()
        self.enroll_code.setPlaceholderText("Code")

        self.enroll_time = QLineEdit()
        self.enroll_time.setPlaceholderText("Time")

        self.enroll_room = QLineEdit()
        self.enroll_room.setPlaceholderText("Room")

        enroll_button = QPushButton("Enroll")
        enroll_button.clicked.connect(self.enroll)

        enrollment_form.addWidget(QLabel("Course"), 0, 0)
        enrollment_form.addWidget(self.enroll_course, 1, 0)

        enrollment_form.addWidget(QLabel("Code"), 0, 1)
        enrollment_form.addWidget(self.enroll_code, 1, 1)

        enrollment_form.addWidget(QLabel("Time"), 0, 2)
        enrollment_form.addWidget(self.enroll_time, 1, 2)

        enrollment_form.addWidget(QLabel("Room"), 0, 3)
        enrollment_form.addWidget(self.enroll_room, 1, 3)

        enrollment_form.addWidget(enroll_button, 1, 4)

        layout.addLayout(enrollment_form)

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = QHBoxLayout()
        buttons.addStretch()

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update)

        delete_button = QPushButton("Delete")
        delete_button.setObjectName("danger")
        delete_button.clicked.connect(self.delete)

        buttons.addWidget(update_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.course.currentIndexChanged.connect(self.update_subjects)
        self.year_level.currentIndexChanged.connect(self.update_subjects)

        self.load_course_choices()

    def load_student(self, student_id):
        self.student_id = student_id

        student = service.get_one(student_id)

        if not student:
            QMessageBox.warning(self, "Error", "Student not found.")
            self.main_window.show_students()
            return

        self.fill_form(student)

        self.update_subjects()
        self.load_enrollments()

    def load_enrollments(self):
        self.enrollment_table.setRowCount(0)

        enrollments = service.get_enrollments(self.student_id)

        for row, enrollment in enumerate(enrollments):
            # ENROLLMENT_COLUMNS: id, student_id, course_code, code, time, room
            self.enrollment_table.insertRow(row)

            for column, index in enumerate([2, 3, 4, 5]):
                self.enrollment_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(enrollment[index]))
                )

            remove_button = QPushButton("Remove")
            remove_button.setObjectName("view")

            remove_button.clicked.connect(
                lambda checked=False, enrollment_id=enrollment[0]:
                self.remove_enrollment(enrollment_id)
            )

            self.enrollment_table.setCellWidget(row, 4, remove_button)

    def enroll(self):
        enrollment_id, title, message = service.enroll(
            self.student_id,
            self.enroll_course.currentText(),
            self.enroll_code.text().strip(),
            self.enroll_time.text().strip(),
            self.enroll_room.text().strip()
        )

        if title:
            QMessageBox.warning(self, title, message)
            return

        self.enroll_code.clear()
        self.enroll_time.clear()
        self.enroll_room.clear()

        self.load_enrollments()

    def remove_enrollment(self, enrollment_id):
        service.unenroll(enrollment_id)

        self.load_enrollments()

    def update(self):
        success, title, message = service.update(
            self.student_id,
            self.read_form()
        )

        if not success:
            QMessageBox.warning(self, title, message)
            return

        QMessageBox.information(
            self,
            "Updated",
            "Student information updated successfully."
        )

        self.main_window.show_students()

    def delete(self):
        answer = QMessageBox.question(
            self,
            "Delete Student",
            "Are you sure you want to delete this student?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            service.delete(self.student_id)

            QMessageBox.information(self, "Deleted", "Student deleted successfully.")
            self.student_id = None
            self.main_window.show_students()

        except Exception as e:
            QMessageBox.critical(self, "Delete Error", f"Failed to delete students: \n{e}")
