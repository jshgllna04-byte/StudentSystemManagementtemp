from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QListWidget,QMessageBox)
from database import add_student
from subjects import get_subjects

class VerifyStudentPage(QWidget):
    def __init__(self,main_window):
        super(). __init__()

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
        form.addWidget(
            QLabel("Full name:"),
            0, 0
        )

        form.addWidget(
            self.fullname,
            0, 1
        )

        form.addWidget(
            QLabel("Age:"),
            1, 0
        )

        form.addWidget(
            self.age,
            1, 1
        )

        form.addWidget(
            QLabel("Address:"),
            2, 0
        )

        form.addWidget(
            self.address,
            2, 1
        )

        form.addWidget(
            QLabel("Contact:"),
            3, 0
        )

        form.addWidget(
            self.contact,
            3, 1
        )

        form.addWidget(
            QLabel("Email:"),
            4, 0
        )

        form.addWidget(
            self.email,
            4, 1
        )

        # Right side
        form.addWidget(
            QLabel("Course:"),
            0, 2
        )

        form.addWidget(
            self.course,
            0, 3
        )

        form.addWidget(
            QLabel("Year Level:"),
            0, 4
        )

        form.addWidget(
            self.year_level,
            0, 5
        )

        form.addWidget(
            QLabel("Subjects:"),
            1, 2
        )

        form.addWidget(
            self.subjects,
            1, 3,
            4, 3
        )

        layout.addLayout(form)

        # Buttons
        buttons = QHBoxLayout()

        back_button = QPushButton(
            "Back"
        )

        back_button.clicked.connect(
            self.main_window.show_add_student
        )

        submit_button = QPushButton(
            "Submit"
        )

        submit_button.clicked.connect(
            self.submit
        )

        buttons.addStretch()
        buttons.addWidget(back_button)
        buttons.addWidget(submit_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self.setLayout(layout)

    def load_data(self, data):

        self.fullname.setText(
            data["fullname"]
        )

        self.age.setText(
            str(data["age"])
        )

        self.address.setText(
            data["address"]
        )

        self.contact.setText(
            data["contact"]
        )

        self.email.setText(
            data["email"]
        )

        self.course.setText(
            data["course"]
        )

        self.year_level.setText(
            data["year_level"]
        )

        self.subjects.clear()

        subjects = get_subjects(
            data["course"],
            data["year_level"]
        )

        for subject in subjects:

            self.subjects.addItem(
                "• " + subject
            )

    def submit(self):

        data = self.main_window.pending_student

        if not data:
            return

        add_student(
            data["fullname"],
            data["age"],
            data["address"],
            data["contact"],
            data["email"],
            data["course"],
            data["year_level"]
        )

        QMessageBox.information(
            self,
            "Success",
            "Student added successfully!"
        )

        self.main_window.pending_student = None

        self.main_window.show_dashboard()
