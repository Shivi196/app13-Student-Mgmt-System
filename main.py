import sqlite3
import sys
from idlelib.help_about import AboutDialog
from pty import CHILD

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QPushButton, \
    QVBoxLayout, QToolBar, QStatusBar, QMessageBox


# from PyQt6.QtWidgets.QMainWindow import statusBar

class DatabaseConnection():
    def __init__(self,database_file= "database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Set the title for the GUI App
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)

        # Add a MenuBar items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add the subitem  Add Student of File item in MenuBar
        add_student_action = QAction(QIcon("icons/add.png"),"Add Student",self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        # Add the subitem  About of Help item in MenuBar
        about_action = QAction("About",self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole) #this line is for mac users who can't see help icon in menubar
        about_action.triggered.connect(self.about)

#         Add the subitem Search of Edit item in Menubar
        search_action = QAction(QIcon("icons/search.png"),"Search",self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)


#       Add table to the centre of the widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False) #make the index col invisible from the gui
        self.setCentralWidget(self.table)

        # Create toolbar and Add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(search_action)
        toolbar.addAction(add_student_action)

    #     Create statusbar and add statusbar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell clicked
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
#       Populate SQL table with Data
        connection = DatabaseConnection().connect()
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

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students(name,course,mobile) VALUES (?,?,?)",(name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()  #for loading the insert data on run time in the main window

class SearchDialog(QDialog):

    def __init__(self):
        super().__init__()
        # Set search window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name")
        layout.addWidget(self.search_name)

        # Create Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_student)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_student(self):
        name = self.search_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute(f"Select * FROM students where name = ?",(name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Students Dialog")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name and id  from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index,1).text()
        self.student_id = main_window.table.item(index,0).text()

        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box for Courses

        self.course_name = QComboBox()
        courses = (["Biology","Physics","Mathematics","Astronomy"])
        self.course_name.addItems(courses)
        course_name = main_window.table.item(index, 2).text()
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        self.update = QPushButton("Update")
        self.update.clicked.connect(self.update_students)
        layout.addWidget(self.update)

        self.setLayout(layout)

    def update_students(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students set name = ?, course = ? , mobile = ? WHERE id = ?",
                       (
                           self.student_name.text(),
                           self.course_name.currentText(), #alternative of currentText is : self.course_name.itemText(self.course_name.currentIndex()),
                           self.mobile.text(),
                           self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

#         Refresh the Table in main window
        main_window.load_data()
        self.close()

        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Success")
        confirmation_message.setText("Updated record success!")
        confirmation_message.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Students")

        layout = QGridLayout()

        confirmation = QLabel("Do you really wanna delete it ?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete)

    def delete(self):

        # Get the selected id and row for deleting records
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students where id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close() #this will help in closing the  dialog box which ask for yes nd no confirmation

        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Success")
        confirmation_message.setText("The record was successfully deleted!!")
        confirmation_message.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """ This is About page of my Student system mgmt App /
        Feel free to use this code.. thanks!!
        """
        self.setText(content)

# Routine call for running gui app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
