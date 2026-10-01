from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from database import authentication

class LoginPage(QWidget):
    def __init__(self, main_window):
        super(). __init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(250, 120, 250, 80)

        title = QLabel("Student Management System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_title = QLabel("Login")
        login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_title.setStyleSheet("font-size: 24px; font-weight: bold")
        
        

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.main_window.show_register)

        layout.addWidget(title)
        layout.addSpacing(25)
        layout.addWidget(login_title)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)

        layout.addSpacing(12)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)

        layout.addSpacing(20)

        layout.addWidget(login_btn)
        layout.addSpacing(12)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def clear_fields(self):
        self.username.clear()
        self.password.clear()

    def login(self):

        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self,"Invalid information", "please enter username and password")
            return

        user = authentication(username, password)

        if user:
            self.main_window.current_user = user
            self.main_window.show_dashboard()

        else:
            QMessageBox.warning(self,"Login Failed", "Invalid Username or Password")