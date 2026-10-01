from PyQt6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QLineEdit,QPushButton, QComboBox,QListWidget,QMessageBox)

from subjects import get_subjects

class AddStudentPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        backbtn = QPushButton("Back")
        backbtn.setObjectName("back")
        backbtn.clicked.connect(self.main_window.show_dashboard)
        top_layout.addWidget(backbtn)
        

        title = QLabel("Add student")
        title.setObjectName("pageTitle")

        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        form = QGridLayout()

        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Enter Fullname")

        self.address = QLineEdit()
        self.address.setPlaceholderText("Enter Address")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Enter age")

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Enter Contact")

        self.course = QComboBox()

        self.course.addItems(["BSCS","BSIT","BSCpE"])

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email")

        self.yearlvl = QComboBox()

        self.yearlvl.addItems(["1st","2nd","3rd","4th","5th"])

        self.subjects = QListWidget()

        form.addWidget(QLabel("Fullname"),0,0)
        form.addWidget(self.fullname,1,0)

        form.addWidget(QLabel("Address"),0,1)
        form.addWidget(self.address,1,1)

        form.addWidget(QLabel("age"),2,0)
        form.addWidget(self.age,3,0)

        form.addWidget(QLabel("Contact"),2,1)
        form.addWidget(self.contact,3,1)

        form.addWidget(QLabel("Course"),4,0)
        form.addWidget(self.course,5,0)

        form.addWidget(QLabel("Email"),4,1)
        form.addWidget(self.email,5,1)

        form.addWidget(QLabel("Year Level"),6,0)
        form.addWidget(self.yearlvl,7,0)

        form.addWidget(QLabel("Subjects"),6,1)
        form.addWidget(self.subjects,7,1)

        main_layout.addLayout(form)


        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        nextbtn = QPushButton("Next>")
        nextbtn.setFixedWidth(150)
        nextbtn.clicked.connect(self.next_page)

        btn_layout.addWidget(nextbtn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        self.course.currentIndexChanged.connect(self.update_subjects)

        self.yearlvl.currentIndexChanged.connect(self.update_subjects)

        self.update_subjects()

    def clear_form(self):
        self.fullname.clear()
        self.age.clear()
        self.address.clear()
        self.contact.clear()
        self.email.clear()

        self.course.setCurrentIndex(0)
        self.yearlvl.setCurrentIndex(0)

    def update_subjects(self):
        self.subjects.clear()

        course = self.course.currentText()
        year = self.yearlvl.currentText()

        subjects = get_subjects(course,year)

        for subject in subjects:
            self.subjects.addItem(
                "." + subject
            )

    def next_page(self):
        fullname =self.fullname.text().strip()
        age = self.age.text().strip()
        address = self.address.text().strip()
        contact = self.contact.text().strip()
        email = self.email.text().strip()

        if not fullname:
            QMessageBox.warning(self,"Missing information", "Please enter the fullname.")
            return
        if not age:
            QMessageBox.warning(self,"Missing information", "Please enter the age.")
            return
        if not address:
            QMessageBox.warning(self,"Missing information", "Please enter the address.")
            return
        if not contact:
            QMessageBox.warning(self,"Missing information", "Please enter the contact.")
            return
        if not email:
            QMessageBox.warning(self,"Missing Information","Please enter the email.")
            return

        try:
            age_number = int(age)
            if age_number <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self,"Invalid Age","Age must be a valid number")
            return
        
        if not address:
            QMessageBox.warning(self,"Missing Information","Please enter the address.")

            return

        if not contact:
            QMessageBox.warning(self,"Missing Information","Please enter the contact.")
            return

        if not email:
            QMessageBox.warning(self,"Missing Information","Please enter the email.")
            return

        data = {
            "fullname": fullname,
            "age": age_number,
            "address" : address,
            "contact": contact,
            "email": email,
            "course": self.course.currentText(),
            "year_level": self.yearlvl.currentText()}

        self.main_window.pending_student = data

        self.main_window.verify_page.load_data(data)
        self.main_window.show_verify()    
