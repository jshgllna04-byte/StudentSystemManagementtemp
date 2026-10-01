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
from features.student.model import COURSES, YEAR_LEVELS, get_subjects


class AddStudentPage(QWidget):

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

        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Enter Fullname")

        self.address = QLineEdit()
        self.address.setPlaceholderText("Enter Address")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter age")

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Enter Contact")

        self.course = QComboBox()
        self.course.addItems(COURSES)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email")

        self.yearlvl = QComboBox()
        self.yearlvl.addItems(YEAR_LEVELS)

        self.subjects = QListWidget()

        form.addWidget(QLabel("Fullname"), 0, 0)
        form.addWidget(self.fullname, 1, 0)

        form.addWidget(QLabel("Address"), 0, 1)
        form.addWidget(self.address, 1, 1)

        form.addWidget(QLabel("age"), 2, 0)
        form.addWidget(self.age, 3, 0)

        form.addWidget(QLabel("Contact"), 2, 1)
        form.addWidget(self.contact, 3, 1)

        form.addWidget(QLabel("Course"), 4, 0)
        form.addWidget(self.course, 5, 0)

        form.addWidget(QLabel("Email"), 4, 1)
        form.addWidget(self.email, 5, 1)

        form.addWidget(QLabel("Year Level"), 6, 0)
        form.addWidget(self.yearlvl, 7, 0)

        form.addWidget(QLabel("Subjects"), 6, 1)
        form.addWidget(self.subjects, 7, 1)

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
        self.yearlvl.currentIndexChanged.connect(self.update_subjects)

        self.update_subjects()

    def clear_form(self):
        self.fullname.clear()
        self.age.clear()
        self.address.clear()
        self.contact.clear()
        self.email.clear()

        self.course.setCurrentIndex(0)
        self.yearlvl.setCurrentIndex(0)

    def update_subjects(self):
        self.subjects.clear()

        for subject in get_subjects(
            self.course.currentText(),
            self.yearlvl.currentText()
        ):
            self.subjects.addItem("." + subject)

    def next_page(self):
        data = {
            "fullname": self.fullname.text().strip(),
            "age": self.age.text().strip(),
            "address": self.address.text().strip(),
            "contact": self.contact.text().strip(),
            "email": self.email.text().strip(),
            "course": self.course.currentText(),
            "year_level": self.yearlvl.currentText()
        }

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

        self.fullname = QLabel()
        self.age = QLabel()
        self.address = QLabel()
        self.contact = QLabel()
        self.email = QLabel()

        self.course = QLabel()
        self.year_level = QLabel()

        self.subjects = QListWidget()

        # Left side
        form.addWidget(QLabel("Full name:"), 0, 0)
        form.addWidget(self.fullname, 0, 1)

        form.addWidget(QLabel("Age:"), 1, 0)
        form.addWidget(self.age, 1, 1)

        form.addWidget(QLabel("Address:"), 2, 0)
        form.addWidget(self.address, 2, 1)

        form.addWidget(QLabel("Contact:"), 3, 0)
        form.addWidget(self.contact, 3, 1)

        form.addWidget(QLabel("Email:"), 4, 0)
        form.addWidget(self.email, 4, 1)

        # Right side
        form.addWidget(QLabel("Course:"), 0, 2)
        form.addWidget(self.course, 0, 3)

        form.addWidget(QLabel("Year Level:"), 0, 4)
        form.addWidget(self.year_level, 0, 5)

        form.addWidget(QLabel("Subjects:"), 1, 2)
        form.addWidget(self.subjects, 1, 3, 4, 3)

        layout.addLayout(form)

        # Buttons
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
        self.fullname.setText(data["fullname"])
        self.age.setText(str(data["age"]))
        self.address.setText(data["address"])
        self.contact.setText(data["contact"])
        self.email.setText(data["email"])
        self.course.setText(data["course"])
        self.year_level.setText(data["year_level"])

        self.subjects.clear()

        for subject in get_subjects(data["course"], data["year_level"]):
            self.subjects.addItem("• " + subject)

    def submit(self):
        data = self.main_window.pending_student

        if not data:
            return

        student_id, title, message = service.create(data)

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
        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Age",
            "Course",
            "Year Level",
            "Address",
            "Contact",
            "Email",
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

        for row, student in enumerate(students):
            self.table.insertRow(row)

            for column in range(8):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(student[column]))
                )

            view_button = QPushButton("View")
            view_button.setObjectName("view")

            view_button.clicked.connect(
                lambda checked=False, student_id=student[0]:
                self.open_student(student_id)
            )

            self.table.setCellWidget(row, 8, view_button)

    def search_students(self, text):
        text = text.lower().strip()

        if not text:
            self.display_students(self.students)
            return

        filtered = []

        for student in self.students:
            name = str(student[1]).lower()
            email = str(student[7]).lower()

            if text in name or text in email:
                filtered.append(student)

        self.display_students(filtered)

    def open_student(self, student_id):
        self.main_window.show_student_details(student_id)


class StudentDetailsPage(QWidget):

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

        self.fullname = QLineEdit()
        self.age = QLineEdit()
        self.address = QLineEdit()
        self.contact = QLineEdit()
        self.email = QLineEdit()

        self.course = QComboBox()
        self.course.addItems(COURSES)

        self.year_level = QComboBox()
        self.year_level.addItems(YEAR_LEVELS)

        self.subjects = QListWidget()

        form.addWidget(QLabel("Fullname"), 0, 0)
        form.addWidget(self.fullname, 1, 0)

        form.addWidget(QLabel("Address"), 0, 1)
        form.addWidget(self.address, 1, 1)

        form.addWidget(QLabel("Age"), 2, 0)
        form.addWidget(self.age, 3, 0)

        form.addWidget(QLabel("Contact"), 2, 1)
        form.addWidget(self.contact, 3, 1)

        form.addWidget(QLabel("Course"), 4, 0)
        form.addWidget(self.course, 5, 0)

        form.addWidget(QLabel("Email"), 4, 1)
        form.addWidget(self.email, 5, 1)

        form.addWidget(QLabel("Year Level"), 6, 0)
        form.addWidget(self.year_level, 7, 0)

        form.addWidget(QLabel("Subjects"), 6, 1)
        form.addWidget(self.subjects, 7, 1)

        layout.addLayout(form)

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = QHBoxLayout()
        buttons.addStretch()

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        buttons.addWidget(update_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.course.currentIndexChanged.connect(self.update_subjects)
        self.year_level.currentIndexChanged.connect(self.update_subjects)

    def load_student(self, student_id):
        self.student_id = student_id

        student = service.get_one(student_id)

        if not student:
            QMessageBox.warning(self, "Error", "Student not found.")
            self.main_window.show_students()
            return

        # Database order:
        #
        # id
        # fullname
        # age
        # address
        # contact
        # email
        # course
        # year_level

        self.fullname.setText(student[1])
        self.age.setText(str(student[2]))
        self.address.setText(student[3])
        self.contact.setText(student[4])
        self.email.setText(student[5])

        course_index = self.course.findText(student[6])

        if course_index >= 0:
            self.course.setCurrentIndex(course_index)

        year_index = self.year_level.findText(student[7])

        if year_index >= 0:
            self.year_level.setCurrentIndex(year_index)

        self.update_subjects()

    def update_subjects(self):
        self.subjects.clear()

        for subject in get_subjects(
            self.course.currentText(),
            self.year_level.currentText()
        ):
            self.subjects.addItem("• " + subject)

    def collect_data(self):
        return {
            "fullname": self.fullname.text().strip(),
            "age": self.age.text().strip(),
            "address": self.address.text().strip(),
            "contact": self.contact.text().strip(),
            "email": self.email.text().strip(),
            "course": self.course.currentText(),
            "year_level": self.year_level.currentText()
        }

    def update(self):
        success, title, message = service.update(
            self.student_id,
            self.collect_data()
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
