from PyQt6.QtWidgets import(QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox)
from database import register_user

class RegisterPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.setContentsMargins(250, 80, 250, 80)

        title = QLabel("Create Account")
        title.setObjectName("pagetitle")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter new Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)


        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.register)

        back_button = QPushButton("Back")
        back_button.setObjectName("back")

        back_button.clicked.connect(
            self.main_window.show_login
        )

        layout.addWidget(title)

        layout.addSpacing(25)

        layout.addWidget(
            QLabel("Username")
        )

        layout.addWidget(
            self.username
        )

        layout.addWidget(
            QLabel("Password")
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            QLabel("Confirm Password")
        )

        layout.addWidget(
            self.confirm_password
        )

        layout.addSpacing(10)

        layout.addWidget(
            create_btn
        )

        layout.addWidget(
            back_button
        )

        self.setLayout(layout)

    def clear_fields(self):

        self.username.clear()
        self.password.clear()
        self.confirm_password.clear()

    def register(self):

        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm_password.text()

        if not username or not password or not confirm:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in all fields."
            )

            return

        if password != confirm:

            QMessageBox.warning(
                self,
                "Password Error",
                "Passwords do not match."
            )

            return

        if len(password) < 4:

            QMessageBox.warning(
                self,
                "Password Error",
                "Password must contain at least 4 characters."
            )

            return

        success = register_user(
            username,
            password
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                "Account created successfully."
            )

            self.main_window.show_login()

        else:

            QMessageBox.warning(
                self,
                "Username Exists",
                "That username is already registered."
            )



