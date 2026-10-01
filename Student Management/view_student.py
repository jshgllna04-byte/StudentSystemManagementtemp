from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)

from database import get_all_students


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

        back_button.clicked.connect(
            self.main_window.show_dashboard
        )

        title = QLabel(
            "Students Information"
        )

        title.setObjectName(
            "sectionTitle"
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
        # SEARCH
        # ----------------------------------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search student..."
        )

        self.search.textChanged.connect(
            self.search_students
        )

        layout.addWidget(
            self.search
        )

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

        layout.addWidget(
            self.table
        )

        self.setLayout(layout)

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    def load_students(self):

        self.search.clear()

        self.students = get_all_students()

        self.display_students(
            self.students
        )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    def display_students(self, students):

        self.table.setRowCount(0)

        for row, student in enumerate(students):

            self.table.insertRow(row)

            # ID
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(student[0])
                )
            )

            # Name
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(student[1])
                )
            )

            # Age
            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(student[2])
                )
            )

            # Course
            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(student[3])
                )
            )

            # Year
            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(student[4])
                )
            )

            # Address
            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(student[5])
                )
            )

            # Contact
            self.table.setItem(
                row,
                6,
                QTableWidgetItem(
                    str(student[6])
                )
            )

            # Email
            self.table.setItem(
                row,
                7,
                QTableWidgetItem(
                    str(student[7])
                )
            )

            # VIEW BUTTON
            view_button = QPushButton(
                "View"
            )

            view_button.setObjectName(
                "view"
            )

            view_button.clicked.connect(
                lambda checked=False,
                student_id=student[0]:
                self.open_student(student_id)
            )

            self.table.setCellWidget(
                row,
                8,
                view_button
            )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    def search_students(self, text):

        text = text.lower().strip()

        if not text:

            self.display_students(
                self.students
            )

            return

        filtered = []

        for student in self.students:

            name = str(
                student[1]
            ).lower()

            email = str(
                student[7]
            ).lower()

            if (
                text in name
                or text in email
            ):

                filtered.append(
                    student
                )

        self.display_students(
            filtered
        )

    # --------------------------------------------------------
    # OPEN STUDENT
    # --------------------------------------------------------

    def open_student(self, student_id):

        self.main_window.show_student_details(
            student_id
        )


