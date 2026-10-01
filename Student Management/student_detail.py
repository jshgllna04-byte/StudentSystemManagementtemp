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
    QMessageBox
)

from database import (
    get_student,
    update_student,
    delete_student
)

from subjects import get_subjects


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

        back_button = QPushButton(
            "Back"
        )

        back_button.setObjectName(
            "back"
        )

        back_button.setFixedWidth(80)

        back_button.clicked.connect(
            self.main_window.show_students
        )

        title = QLabel(
            "Student Information"
        )

        title.setObjectName(
            "pageTitle"
        )

        top.addWidget(
            back_button
        )

        top.addWidget(
            title
        )

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

        self.course.addItems([
            "BSCS",
            "BSIT",
            "BSCpE"
        ])

        self.year_level = QComboBox()

        self.year_level.addItems([
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th"
        ])

        self.subjects = QListWidget()

        # Fullname
        form.addWidget(
            QLabel("Fullname"),
            0, 0
        )

        form.addWidget(
            self.fullname,
            1, 0
        )

        # Address
        form.addWidget(
            QLabel("Address"),
            0, 1
        )

        form.addWidget(
            self.address,
            1, 1
        )

        # Age
        form.addWidget(
            QLabel("Age"),
            2, 0
        )

        form.addWidget(
            self.age,
            3, 0
        )

        # Contact
        form.addWidget(
            QLabel("Contact"),
            2, 1
        )

        form.addWidget(
            self.contact,
            3, 1
        )

        # Course
        form.addWidget(
            QLabel("Course"),
            4, 0
        )

        form.addWidget(
            self.course,
            5, 0
        )

        # Email
        form.addWidget(
            QLabel("Email"),
            4, 1
        )

        form.addWidget(
            self.email,
            5, 1
        )

        # Year
        form.addWidget(
            QLabel("Year Level"),
            6, 0
        )

        form.addWidget(
            self.year_level,
            7, 0
        )

        # Subjects
        form.addWidget(
            QLabel("Subjects"),
            6, 1
        )

        form.addWidget(
            self.subjects,
            7, 1
        )

        layout.addLayout(form)

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = QHBoxLayout()

        buttons.addStretch()

        update_button = QPushButton(
            "Update"
        )

        update_button.clicked.connect(
            self.update
        )

        delete_button = QPushButton(
            "Delete"
        )

        delete_button.clicked.connect(
            self.delete
        )

        buttons.addWidget(
            update_button
        )

        buttons.addWidget(
            delete_button
        )

        buttons.addStretch()

        layout.addLayout(
            buttons
        )

        self.setLayout(
            layout
        )

        # Update subjects when changed
        self.course.currentIndexChanged.connect(
            self.update_subjects
        )

        self.year_level.currentIndexChanged.connect(
            self.update_subjects
        )

    # --------------------------------------------------------
    # LOAD STUDENT
    # --------------------------------------------------------

    def load_student(self, student_id):

        self.student_id = student_id

        student = get_student(
            student_id
        )

        if not student:

            QMessageBox.warning(
                self,
                "Error",
                "Student not found."
            )

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

        self.fullname.setText(
            student[1]
        )

        self.age.setText(
            str(student[2])
        )

        self.address.setText(
            student[3]
        )

        self.contact.setText(
            student[4]
        )

        self.email.setText(
            student[5]
        )

        course_index = self.course.findText(
            student[6]
        )

        if course_index >= 0:

            self.course.setCurrentIndex(
                course_index
            )

        year_index = self.year_level.findText(
            student[7]
        )

        if year_index >= 0:

            self.year_level.setCurrentIndex(
                year_index
            )

        self.update_subjects()

    # --------------------------------------------------------
    # SUBJECTS
    # --------------------------------------------------------

    def update_subjects(self):

        self.subjects.clear()

        course = self.course.currentText()
        year = self.year_level.currentText()

        subjects = get_subjects(
            course,
            year
        )

        for subject in subjects:

            self.subjects.addItem(
                "• " + subject
            )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self):

        fullname = self.fullname.text().strip()
        age = self.age.text().strip()
        address = self.address.text().strip()
        contact = self.contact.text().strip()
        email = self.email.text().strip()

        course = self.course.currentText()
        year = self.year_level.currentText()

        if not fullname or not age or not address or not contact or not email:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in all fields."
            )

            return

        try:

            age = int(age)

            if age <= 0:
                raise ValueError

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Age",
                "Age must be a valid number."
            )

            return

        update_student(
            self.student_id,
            fullname,
            age,
            address,
            contact,
            email,
            course,
            year
        )

        QMessageBox.information(
            self,
            "Updated",
            "Student information updated successfully."
        )

        self.main_window.show_students()

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

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

            delete_student(self.student_id)

            QMessageBox.information(self,"Deleted","Student deleted successfully.")
            self.student_id=None
            self.main_window.show_students()

        except Exception as e:
            QMessageBox.critical(self,"Delete Error",f"Failed to delete students: \n{e}")


