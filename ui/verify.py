from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)

from database.database import add_student


class VerifyPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window
        self.data = {}

        self.layout = QVBoxLayout()

        title = QLabel("Verify Student Information")
        self.layout.addWidget(title)

        self.info = QLabel()
        self.layout.addWidget(self.info)

        self.subjects_layout = QVBoxLayout()
        self.layout.addLayout(self.subjects_layout)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_student)
        self.layout.addWidget(self.submit_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)


    def load_data(self, data):

        self.data = data

        text = (
            "Full Name: " + data["fullname"] + "\n"
            "Age: " + str(data["age"]) + "\n"
            "Address: " + data["address"] + "\n"
            "Contact: " + data["contact"] + "\n"
            "Email: " + data["email"] + "\n"
            "Course: " + data["course"] + "\n"
            "Year Level: " + data["year_level"]
        )

        self.info.setText(text)

        self.show_subjects()


    def show_subjects(self):

        while self.subjects_layout.count():

            item = self.subjects_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        title = QLabel("Selected Subjects")
        self.subjects_layout.addWidget(title)

        subjects = self.data["subjects"]

        for subject in subjects:

            row = QHBoxLayout()

            label = QLabel(subject)
            row.addWidget(label)

            delete_button = QPushButton("Delete")

            delete_button.clicked.connect(
                lambda checked=False, name=subject:
                self.delete_subject(name)
            )

            row.addWidget(delete_button)

            self.subjects_layout.addLayout(row)


    def delete_subject(self, subject):

        if subject in self.data["subjects"]:

            self.data["subjects"].remove(subject)

        self.show_subjects()


    def submit_student(self):

        if len(self.data["subjects"]) == 0:

            QMessageBox.warning(
                self,
                "Error",
                "Please select at least one subject."
            )

            return

        add_student(
            self.data["fullname"],
            self.data["age"],
            self.data["address"],
            self.data["contact"],
            self.data["email"],
            self.data["course"],
            self.data["year_level"],
            self.data["subjects"]
        )

        QMessageBox.information(
            self,
            "Success",
            "Student added successfully."
        )

        self.main_window.pending_student = None

        self.main_window.show_dashboard()


    def go_back(self):

        self.main_window.add_student_page.selected_subjects.clear()

        for subject in self.data["subjects"]:

            self.main_window.add_student_page.selected_subjects.addItem(
                subject
            )

        self.main_window.add_student_page.selected_label.setText(
            "Selected Subjects: "
            + str(len(self.data["subjects"]))
            + "/10"
        )

        self.main_window.show_add_student()