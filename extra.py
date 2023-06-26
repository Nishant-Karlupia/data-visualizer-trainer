import sys
from PyQt5.QtWidgets import QApplication, QMessageBox,QMainWindow,QPushButton
from PyQt5 import QtCore

class FramelessMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def showEvent(self, event):
        super().showEvent(event)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        btn=QPushButton("Click",self)
        btn.clicked.connect(self.show_another)

    def show_another(self):

        self.message_box = FramelessMessageBox()
        self.message_box.setText("This is a frameless message box.")
        self.message_box.show()


if __name__=="__main__":
    app = QApplication([])
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
    
