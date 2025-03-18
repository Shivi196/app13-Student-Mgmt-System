import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QMainWindow, \
    QTableWidget


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
        file_menu_item.addAction(add_student_action)

        # Add the subitem  About of Help item in MenuBar
        about_action = QAction("About",self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

#       Add table to the centre of the widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.setCentralWidget(self.table)

# Routine call for running gui app
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
