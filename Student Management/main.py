import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget
)

from data.data import create_database

from view import DashboardPage, STYLE

from features.auth import LoginPage, RegisterPage

from features.student import (
    AddStudentPage,
    VerifyStudentPage,
    ViewStudentPage,
    StudentDetailsPage
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Student Management System"
        )

        self.setMinimumSize(
            1100,
            700
        )

        # Current logged-in user
        self.current_user = None

        # Temporary student data
        self.pending_student = None

        # Currently selected student
        self.editing_student_id = None

        # ----------------------------------------------------
        # STACKED WIDGET
        # ----------------------------------------------------

        self.stack = QStackedWidget()

        self.setCentralWidget(
            self.stack
        )

        # ----------------------------------------------------
        # CREATE PAGES
        # ----------------------------------------------------

        self.login_page = LoginPage(
            self
        )

        self.register_page = RegisterPage(
            self
        )

        self.dashboard_page = DashboardPage(
            self
        )

        self.add_student_page = AddStudentPage(
            self
        )

        self.verify_page = VerifyStudentPage(
            self
        )

        self.view_student_page = ViewStudentPage(
            self
        )

        self.student_details_page = StudentDetailsPage(
            self
        )

        # ----------------------------------------------------
        # ADD PAGES TO STACK
        # ----------------------------------------------------

        self.pages = [
            self.login_page,
            self.register_page,
            self.dashboard_page,
            self.add_student_page,
            self.verify_page,
            self.view_student_page,
            self.student_details_page
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        # Start at login
        self.show_login()

    # ========================================================
    # NAVIGATION
    # ========================================================

    def show_login(self):

        self.login_page.clear_fields()

        self.stack.setCurrentWidget(
            self.login_page
        )

    def show_register(self):

        self.register_page.clear_fields()

        self.stack.setCurrentWidget(
            self.register_page
        )

    def show_dashboard(self):

        self.stack.setCurrentWidget(
            self.dashboard_page
        )

    def show_add_student(self):

        self.add_student_page.clear_form()

        self.stack.setCurrentWidget(
            self.add_student_page
        )

    def show_verify(self):

        self.stack.setCurrentWidget(
            self.verify_page
        )

    def show_students(self):

        self.view_student_page.load_students()

        self.stack.setCurrentWidget(
            self.view_student_page
        )

    def show_student_details(self, student_id):

        self.editing_student_id = student_id

        self.student_details_page.load_student(
            student_id
        )

        self.stack.setCurrentWidget(
            self.student_details_page
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        self.current_user = None
        self.pending_student = None

        self.show_login()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    create_database()

    # Apply stylesheet
    app.setStyleSheet(
        STYLE
    )

    window = MainWindow()

    window.show()

    sys.exit(app.exec())
