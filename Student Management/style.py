STYLE = """
QWidget {
    font-family: Arial;
    font-size: 13px;
}

QLineEdit, QComboBox {
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 7px;
    background: white;
}

QLineEdit:focus,
QComboBox:focus {
    border: 1px solid #8c45e8;
}

QPushButton {
    background-color: #2c2c2c;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 9px;
}

QPushButton:hover {
    background-color: #444444;
}

QPushButton#danger {
    background-color: #f02020;
}

QPushButton#danger:hover {
    background-color: #d71919;
}

QPushButton#back {
    background-color: #333333;
}

QPushButton#view {
    padding: 5px 12px;
}

QLabel#title {
    font-size: 28px;
    font-weight: bold;
}

QLabel#pageTitle {
    font-size: 28px;
    font-weight: bold;
}

QLabel#sectionTitle {
    font-size: 20px;
    font-weight: bold;
}

QTableWidget {
    border: 1px solid #dddddd;
    gridline-color: #dddddd;
}

QHeaderView::section {
    background-color: #eeeeee;
    padding: 7px;
    border: none;
    font-weight: bold;
}

QListWidget {
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 7px;
}
"""