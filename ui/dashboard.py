from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class DashboardPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        title = QLabel("Student Management System")
        layout.addWidget(title)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(
            self.main_window.show_add_student
        )
        layout.addWidget(add_button)

        view_button = QPushButton("View Students")
        view_button.clicked.connect(
            self.view_students
        )
        layout.addWidget(view_button)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(
            self.main_window.show_login
        )
        layout.addWidget(logout_button)

        self.setLayout(layout)


    def view_students(self):

        self.main_window.view_student_page.load_students()

        self.main_window.show_view_student()