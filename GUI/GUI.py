from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QMenuBar,
    QStatusBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette
import sys


class MainWindow(QMainWindow):

    def __init__(self):
            super().__init__()
            self.setWindowTitle("TestGUI")
            self.setMinimumSize(1000,540)
            self.setStatusBar(QStatusBar())
            self.setStyleSheet(""" 
                                QMainWindow{
                                backround-color: white;
                                }
                                """)
            pass


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

