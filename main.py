import sqlite3
import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QPushButton, \
    QVBoxLayout


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Set the title for the GUI App
        self.setWindowTitle("Student Management System")

        # Add a MenuBar items
        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        # Add the subitem  Add Student of File item in MenuBar
        add_student_action = QAction("Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add the subitem  About of Help item in MenuBar
        about_action = QAction("About",self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

#       Add table to the centre of the widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False) #make the index col invisible from the gui
        self.setCentralWidget(self.table)

    def load_data(self):
#       Populate SQL table with Data
        connection = sqlite3.Connection("database.db")
        data = connection.execute("SELECT * FROM students")
        # print(list(data))
#  below code set rows to 0 so that duplicates won't enter everytime code runs
        self.table.setRowCount(0)
# Connecting the table structure with the data in database
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number,column_data in enumerate(row_data):
                print(row_data)
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(column_data)))
        connection.close()

    def insert(self):
        insert_dialog = InsertDialog()
        insert_dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Students Dialog")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box for Courses
        self.course_name = QComboBox()
        courses = (["Biology","Physics","Mathematics","Astronomy"])
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        self.register = QPushButton("Register")
        self.register.clicked.connect(self.add_students)
        layout.addWidget(self.register)

        self.setLayout(layout)

    def add_students(self):

        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex()) #you can use directly self.course.currentText() method instead of itemText
        mobile = self.mobile.text()
        connection = sqlite3.Connection("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO STUDENTS (name,course,mobile) VALUES (?,?,?)",(name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()  #for loading the insert data on run time in the main window


# Routine call for running gui app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
