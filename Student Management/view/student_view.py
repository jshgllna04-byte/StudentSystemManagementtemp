from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class DashboardPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(150, 80, 150, 180)

        welcome = QLabel("Welcome to!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Student Management System")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("font-size: 27px; font-weight: bold;")

        addbtn = QPushButton("Add Student")
        addbtn.clicked.connect(self.main_window.show_add_student)

        viewbtn = QPushButton("View")
        viewbtn.clicked.connect(self.main_window.show_students)

        logoutbtn = QPushButton("Logout")
        logoutbtn.setObjectName("danger")
        logoutbtn.clicked.connect(self.main_window.logout)

        layout.addWidget(welcome)
        layout.addWidget(title)

        layout.addSpacing(40)

        layout.addWidget(addbtn)
        layout.addSpacing(15)

        layout.addWidget(viewbtn)

        layout.addStretch()

        layout.addWidget(logoutbtn)

        self.setLayout(layout)
