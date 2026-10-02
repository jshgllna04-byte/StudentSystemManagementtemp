from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class StudentDetailPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Student Details")
        layout.addWidget(title)

        self.info = QLabel()
        layout.addWidget(self.info)

        self.subjects = QLabel()
        layout.addWidget(self.subjects)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(
            self.go_back
        )

        layout.addWidget(self.back_button)

        self.setLayout(layout)


    def load_student(self, student):

        if student is None:
            return

        self.info.setText(
            "ID: " + str(student[0]) + "\n"
            "Full Name: " + student[1] + "\n"
            "Age: " + str(student[2]) + "\n"
            "Address: " + student[3] + "\n"
            "Contact: " + student[4] + "\n"
            "Email: " + student[5] + "\n"
            "Course: " + student[6] + "\n"
            "Year Level: " + student[7]
        )

        subject_text = "Subjects:\n"

        if student[8]:

            import json

            subjects = json.loads(student[8])

            for subject in subjects:

                subject_text += "• " + subject + "\n"

        else:

            subject_text += "No subjects"

        self.subjects.setText(subject_text)


    def go_back(self):

        self.main_window.show_dashboard()